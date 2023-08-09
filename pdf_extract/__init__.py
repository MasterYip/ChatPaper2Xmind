from fileinput import filename
from hashlib import md5
import random
import re
import time
import fitz
import os
import tempfile
import numpy as np
from os import path as op
import subprocess
import json
# FIXME: this is not robust
from config import *

TEMP_DIR = tempfile.mkdtemp()
DIR_PATH = op.dirname(op.abspath(__file__))
PDF_FIGURES_JAR_PATH = op.join(
    DIR_PATH, "pdffigures2", "pdffigures2-assembly-0.0.12-SNAPSHOT.jar"
)

#######################
##  Misc. Functions  ##
#######################

# debugging
def draw_all_textbbox(pdf, colorList=[(1,0,0),(0,1,0),(1,0,1)],
                      widthList=[2,1,0.4]):
    """ draw all text bbox(block/line/span) in pdf"""
    for page in pdf:
        blocks = page.get_text("dict", flags=0)["blocks"]
        for block in blocks:
            page.draw_rect(block['bbox'], color=colorList[0], width=widthList[0])
            for line in block['lines']:
                page.draw_rect(line['bbox'], color=colorList[1], width=widthList[1])
                for span in line['spans']:
                    page.draw_rect(span['bbox'], color=colorList[2], width=widthList[2])


def draw_all_drawingbbox(pdf, color=(1, 0, 0), width=1):
    """ draw all drawing bbox in pdf"""
    for page in pdf:
        paths = page.get_drawings()
        for path in paths:
            page.draw_rect(path['rect'], color=color, width=width)


def draw_all_imagebbox(pdf, color=(0, 1, 0), width=2):
    """ draw all image bbox in pdf"""
    for page in pdf:
        images = page.get_images(full=True)
        for img in images:
            page.draw_rect(page.get_image_bbox(img), color=color, width=width)

# FIXME
def draw_all_svgbbox(pdf, color=(0.3, 0.3, 1), width=2):
    """ draw all svg bbox in pdf"""
    for page in pdf:
        svgs = page.get_svg_image()
        print(svgs)
        for svg in svgs:
            page.draw_rect(svg[0:4], color=color, width=width)

# utils
def rand_color():
    r = random.random()
    g = random.random()
    b = random.random()
    return (r, g, b)


def get_current_time():
    """
    Get the current time in milliseconds
    """
    return int(round(time.time() * 1000))


def generate_id():
    """
    Generate unique 26-digit random string
    """
    # FIXME: Why not use something like the builtin uuid.uuid1() method?
    # md5 current time get 32-digit random string
    timestamp = md5(str(get_current_time()).encode('utf-8')).hexdigest()
    lotter = md5(str(random.random()).encode('utf-8')).hexdigest()
    _id = timestamp[19:] + lotter[:13]
    return _id


def is_inbox(point, bbox):
    if bbox[0] < point[0] < bbox[2] and bbox[1] < point[1] < bbox[3]:
        return True
    else:
        return False


def get_bounding_box(bbox_cluster_list):
    if bbox_cluster_list:
        x0 = min([bbox[0] for bbox in bbox_cluster_list])
        y0 = min([bbox[1] for bbox in bbox_cluster_list])
        x1 = max([bbox[2] for bbox in bbox_cluster_list])
        y1 = max([bbox[3] for bbox in bbox_cluster_list])
        return (x0, y0, x1, y1)
    else:
        return None


def box_center(bbox):
    return ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)


def get_objpixmap(pdf, obj, zoom=4, savepath=None, get_tmpfile_dir=True):
    """
    Get pixmap(tmp_path) of the object
    
    :param pdf: pdf file
    :param obj: object tuple (text position, page number, bbox)
    :param zoom: zoom of the object
    :param savepath: save path of the object
    :return: pixmap of the object
    """
    page = pdf[obj[1]]
    box = obj[2]
    pixmap = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=box)
    if savepath and os.path.isdir(savepath):
        pixmap.save(savepath)
    if get_tmpfile_dir:
        tmp_path = os.path.join(TEMP_DIR, generate_id()+'.png')
        pixmap.save(tmp_path)
        return tmp_path
    else:
        return pixmap


# Section Judge
def get_plaintext_sample(page, box, sample_len=20):
    blocks = page.get_text("dict", flags=0)["blocks"]
    sample_str = ""
    flag = False
    for block in blocks:
        for line in block['lines']:
            for span in line['spans']:
                if is_inbox(box_center(span['bbox']), box):
                    flag = True
                if flag:
                    sample_str += span['text']
                if len(sample_str) > sample_len:
                    return sample_str
            if flag:
                sample_str += '\n'
    return sample_str  # considering text is all checked


def get_box_textpos(page, box, all_text):
    """ get the position of the box in the all_text
    TODO: This is not a robust method to find the position of the box.
    """
    text = get_plaintext_sample(page, box)
    return all_text.find(text)


##########################################
##  Legacy Method for Eq/Fig Detection  ##
##########################################

# Box Clustering
def bbox_clustering(start_pos, bbox_list, critic_dis=(50, 15), maxnum=50, maxdis=(100, 50)):
    # start_pos: (x0, y0)
    # bbox_list: [(x0, y0, x1, y1)]
    # critic_distant: int
    remain_bbox = bbox_list
    cluster_bbox = []
    cluster_points = [start_pos]
    expand_cnt = 1
    while expand_cnt > 0 and len(cluster_bbox) < maxnum:
        expand_cnt = 0
        for pos in cluster_points:
            for bbox in remain_bbox:
                # Manhattan distance
                center = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
                if abs(center[0] - pos[0]) < critic_dis[0] and abs(center[1] - pos[1]) < critic_dis[1]\
                        and abs(center[0] - start_pos[0]) < maxdis[0] and abs(center[1] - start_pos[1]) < maxdis[1]:
                    cluster_bbox.append(bbox)
                    remain_bbox.pop(remain_bbox.index(bbox))
                    # Center point
                    cluster_points.append(center)
                    expand_cnt += 1

    return cluster_bbox


def bbox_clustering_DBSCAN(start_pos, bbox_list, critic_distant):
    pass


# Equation extract
def get_possible_eqspan(page, draw=False):
    possible_bbox = []
    numbering_bbox = []
    blocks = page.get_text("dict", flags=0)["blocks"]
    for block in blocks:
        # draw bbox of block
        # page.draw_rect(block['bbox'], color=(1, 0, 0), width=2)
        for line in block['lines']:
            # page.draw_rect(line['bbox'], color=(0, 1, 0), width=1)
            for span in line['spans']:
                if span['flags'] == 6:
                    if draw:
                        page.draw_rect(span['bbox'], color=(
                            0.8, 1, 0), width=0.8)
                    possible_bbox.append(span['bbox'])
                # TODO: CMMI CMR MSBM
                if span['font'].startswith('CM') or span['font'].startswith('MSBM'):
                    if draw:
                        page.draw_rect(span['bbox'], color=(
                            0.4, 1, 0), width=0.8)
                    possible_bbox.append(span['bbox'])

                # Numbering
                if re.match(EQUATION_MATCHSTR, span['text']):
                    if draw:
                        page.draw_rect(
                            span['bbox'], color=(0, 0, 1), width=0.4)
                    numbering_bbox.append(span['bbox'])
    return (numbering_bbox, possible_bbox)


def combine_eqbox(bbox, critic_ydis=5):
    """Combine the overlapped equation bounding boxes"""
    bbox_list = bbox
    i = 0
    while i < len(bbox_list)-1:
        if bbox_list[i+1][1]-bbox_list[i][3] < critic_ydis and abs(bbox_list[i+1][0]-bbox_list[i][0]) < 1:
            bounding = get_bounding_box(bbox_list[i:i+2])
            bbox_list.pop(i)
            bbox_list.pop(i)
            bbox_list.insert(i, bounding)
            i -= 1
        i += 1
    return bbox_list


def get_eqbox(page, draw=False):
    page_width = page.bound()[2]
    # page_height = page.bound()[3]
    xmargin = 40
    column1 = (xmargin, page_width/2)
    column2 = (page_width/2, page_width-xmargin)
    numbering_bbox, possible_bbox = get_possible_eqspan(page, draw=draw)
    adp_box_list = []
    # TODO: There are some equation's numbering is a little bit lower than the equation
    start_y_shift = -5
    for num_box in numbering_bbox:
        center = ((num_box[0] + num_box[2]) / 2,
                  (num_box[1] + num_box[3]) / 2)
        start = (center[0] - page_width/5, center[1])
        clustering_box = bbox_clustering((start[0], start[1]+start_y_shift),
                                         possible_bbox, critic_dis=(page_width/8, 10), maxnum=50)
        if draw:
            color = rand_color()
            for box in clustering_box:
                page.draw_rect(box, color=color, width=0.4)
        tar_box = get_bounding_box(clustering_box)
        if tar_box:
            tar_center = ((tar_box[0] + tar_box[2]) / 2,
                          (tar_box[1] + tar_box[3]) / 2)
            # Adapt Box
            adpat_ymargin = 0
            if tar_center[0] < page_width/2:
                adapt_box = (
                    column1[0], tar_box[1]-adpat_ymargin, column1[1], tar_box[3]+adpat_ymargin)
            else:
                adapt_box = (
                    column2[0], tar_box[1]-adpat_ymargin, column2[1], tar_box[3]+adpat_ymargin)
            adp_box_list.append(adapt_box)
            if draw:
                page.draw_rect(adapt_box, color=(1, 0, 0), width=0.8)
    return combine_eqbox(adp_box_list, 10)


def draw_eqbox(pdf):
    for page in pdf:
        adp_box_list = get_eqbox(page, draw=False)
        for adp_box in adp_box_list:
            page.draw_rect(adp_box, color=(0, 1, 0), width=2)

#######################################
##  New Method for Eq/Fig Detection  ## (TODO: Needs refinement)
#######################################

## Compose Detection
# TODO: Not yet stable
def getColumnRect(page, resolution=50, critic=5, margin=5, drawDen=False):
    """ Get the column rect of the page"""
    LBDensity = np.zeros(resolution)
    RBDensity = np.zeros(resolution)
    width = page.bound()[2]
    height = page.bound()[3]
    blocks = page.get_text("dict", flags=0)["blocks"]
    for block in blocks:
        LBDensity[int(np.round(block['bbox'][0]/width*resolution))] += 1
        RBDensity[int(np.round(block['bbox'][2]/width*resolution))] += 1
    Density = LBDensity+RBDensity
    if drawDen:
        plot(range(len(Density)), Density)
    x_seg = []
    column_rects = []
    for x in range(1, resolution-1):
        # find local maximas
        if Density[x-1] <= Density[x] and Density[x] >= Density[x+1]\
        and Density[x] >= critic:
            x_seg.append(x)
    for i in range(len(x_seg)-1):
        column_rects.append([x_seg[i]/resolution*width-margin, 0,
                             x_seg[i+1]/resolution*width+margin, height])
    return column_rects


def getColumnRectLegacy(page, colnum=2, xmargin=40, ymargin=0):
    height = page.bound()[3]
    width = page.bound()[2]
    col1 = [xmargin, ymargin, width/colnum, height-ymargin]
    col2 = [width/colnum, ymargin, width-xmargin, height-ymargin]
    return [col1, col2]


def combineRect(bbox, critic_dis=5, critic_alignerr=10, dir=1):
    """
    Combine the equation bounding boxes
    :param bbox: list of bounding boxes
    :param critic_dis: critical distance of combining direction
    :param critic_alignerr: critical align error of tangential direction
    :param dir: 0 for x direction, 1 for y direction
    """
    
    
    if dir == 1: # y direction
        up = 3; low = 1; up2 = 2; low2 = 0; dir2 = 0
    elif dir == 0:# x direction
        up = 2; low = 0; up2 = 3; low2 = 1; dir2 = 1
    else:
        raise ValueError("dir should be 0 or 1")
    validtag = [1 for i in range(len(bbox))]
    for i in range(len(bbox)-1):
        if validtag[i] == 0:
            continue
        b1 = bbox[i]
        for j in range(i+1, len(bbox)):
            if validtag[j] == 0:
                continue
            b2 = bbox[j]
            if abs(b1[up]+b1[low]-b2[up]-b2[low]) < b1[up]-b1[low] + b2[up]-b2[low] + critic_dis\
                    and abs(b2[low2]-b1[low2]) < critic_alignerr\
                    and abs(b2[up2]-b1[up2]) < critic_alignerr:
                bbox[i] = get_bounding_box([b1, b2])
                validtag[j] = 0
    return [bbox[i] for i in range(len(bbox)) if validtag[i] == 1]


## General Object Detect
def getDensityMap(BoxWeightList, roi: tuple[4],
                  resolution=100, dir=1, slideavg_windowsize=1):
    """ Get the density map of the box list
    
    :param BoxWeightList: list of the box and weight (box[4], weight)
    :param roi: ROI of the density map
    :param resolution: resolution of the density map
    :param dir: direction of the density map ([0, 1], i.e. [x, y])
    :return: density map of the box list (x, density)
    """
    def sliding_average(arr, window_size):
        if window_size == 1:
            return arr
        return np.convolve(arr, np.ones(window_size) / window_size, mode='same')
    
    density = np.zeros(resolution, dtype=np.int32)
    if dir == 1: # y direction
        up = 3; low = 1; up2 = 2; low2 = 0; dir2 = 0
    elif dir == 0:# x direction
        up = 2; low = 0; up2 = 3; low2 = 1; dir2 = 1
    else:
        raise ValueError("dir should be 0 or 1")
    
    def regulateBox(box):
        """ Regulate the box to the resolution"""
        box = list(box)
        box[low] = np.floor((box[low]-roi[low])/(roi[up]-roi[low])*resolution)
        box[up] = np.ceil((box[up]-roi[low])/(roi[up]-roi[low])*resolution)
        return box
    for box, weight in BoxWeightList:
        box = regulateBox(box)
        # if box_center(box)[dir2] < roi[up2] and box_center(box)[dir2] > roi[low2]:
        if (box[up2] < roi[up2] and box[up2] > roi[low2]) or (box[low2] < roi[up2] and box[low2] > roi[low2]):
            density[int(box[low]):int(box[up])] += weight
    return (np.array(range(len(density)))/resolution*(roi[up]-roi[low]), sliding_average(density, slideavg_windowsize))


# Equation Box Detection
def getEqBoxList(page, numbox_margin=5):
    """
    Get the (equation box, numbering box, irregular box) of the page
    
    :param page: page of the pdf
    :param numbox_enlarge: enlarge the numbering box
    """
    eqbox = []
    numbox =[]
    irrbox = []
    blocks = page.get_text("dict", flags=0)["blocks"]
    for block in blocks:
        for line in block['lines']:
            for span in line['spans']:
                # Possible equation span
                if span['flags'] == 6:
                    eqbox.append(span['bbox'])
                # TODO: CMMI CMR MSBM and?
                elif span['font'].startswith('CM') or span['font'].startswith('MSBM'):
                    eqbox.append(span['bbox'])
                # Numbering span
                elif re.match(EQUATION_MATCHSTR, span['text']):
                    box = span['bbox']
                    box = (box[0]-numbox_margin, box[1]-numbox_margin,
                        box[2]+numbox_margin, box[3]+numbox_margin)
                    numbox.append(box)
                else:
                    irrbox.append(span['bbox'])
    return (eqbox, numbox, irrbox)


def getEqBoxWeight(boxLists, weights=[1, 1000, -10]):
    """
    Get the box & weight of possible equation span
    
    :boxLists: (equation box, numbering box, irrelevant box)
    :param weights: weights of [possible equation span, numbering span, irrelevant span]
    """
    BoxWeightList = []
    for box in boxLists[0]:  # Equation box
        BoxWeightList.append((box, weights[0]))
    for box in boxLists[1]:  # Numbering box
        BoxWeightList.append((box, weights[1]))
    for box in boxLists[2]:  # Irrelevant box
        BoxWeightList.append((box, weights[2]))

    return BoxWeightList


def getEquationRectFromMap(denMap, numBoxList, columnROI, c_bias=0, dir=1, dirmargin=0):
    """
    Get the equation rect from the density map
    
    :param denMap: density map of the equation box
    :param numBoxList: list of the numbering box
    :param columnROI: ROI of the column
    :param c_bias: critical bias range computation
    :param dir: direction of the density map ([0, 1], i.e. [x, y])
    :param dirmargin: margin in the direction
    """
    if dir == 1:  # y direction
        up = 3; low = 1; up2 = 2; low2 = 0; dir2 = 0
    elif dir == 0:  # x direction
        up = 2; low = 0; up2 = 3; low2 = 1; dir2 = 1
    EqRects = []
    for box in numBoxList:
        center = list(box_center(box))
        # Shift numbering box center to the center of the column
        center[dir2] -= (columnROI[up2]-columnROI[low2])/2
        if center[dir2] < columnROI[up2] and center[dir2] > columnROI[low2]:
            x_ls = denMap[0]
            index0 = int(center[dir]/x_ls[-1]*len(x_ls))
            ptr_up = index0
            ptr_low = index0
            while ptr_up < len(x_ls)-1 and denMap[1][ptr_up] > c_bias:
                ptr_up += 1
            while ptr_low > 0 and denMap[1][ptr_low] > c_bias:
                ptr_low -= 1
            EqRects.append((columnROI[low2], x_ls[ptr_low]-dirmargin,
                            columnROI[up2], x_ls[ptr_up]+dirmargin))
    return EqRects


def getEqRect(page, drawDen=False):
    """ Get the equation rect of the page"""
    EqRects = []
    boxLists = getEqBoxList(page)
    EqBoxWeight = getEqBoxWeight(boxLists)
    column_rects = getColumnRectLegacy(page)
    for col in column_rects:
        map = getDensityMap(EqBoxWeight, col)
        if drawDen:
            plot(map[0], map[1])
        EqRects += getEquationRectFromMap(map, boxLists[1], col)
    return combineRect(EqRects)


# Figure Box Detection
def getFigBoxList(page):
    """
    Get the figure box list of the page
    :param page: page of the pdf
    :return: (path box, image box, numbering box, irrelevant box)
    """
    pathbox = []
    imgbox = []
    numbox = []
    irrbox = []
    paths = page.get_drawings()
    for path in paths:
        pathbox.append(path['rect'])
    # Image box
    images = page.get_images(full=True)
    for image in images:
        imgbox.append(page.get_image_bbox(image))
    # Numbering block
    blocks = page.get_text("dict", flags=0)["blocks"]
    for block in blocks:
        if re.match(IMG_MATCHSTR, block['lines'][0]['spans'][0]['text']):
            numbox.append(block['bbox'])
            if DEBUG_MODE:
                page.draw_rect(block['bbox'], color=(1, 0, 0), width=1)
        else:# Irrelevant block
            irrbox.append(block['bbox'])
    return (pathbox, imgbox, numbox, irrbox)


def getFigBoxWeight(FigBoxList, weights=[1, 10, 10, -1]):
    """
    Get the box & weight of possible figure area
    
    :FigBoxList: (drawing box, image box, numbering block, irrelevant block)
    :param weights: weights of [drawing box, image box, numbering block, irrelevant block]
    """
    # TODO: svg_image needs to be considered
    BoxWeightList = []
    # Drawing box
    for box in FigBoxList[0]:
        BoxWeightList.append((box, weights[0]))
    # Image box
    for box in FigBoxList[1]:
        BoxWeightList.append((box, weights[1]))
    # Numbering block
    for box in FigBoxList[2]:
        BoxWeightList.append((box, weights[2]))
    # Irrelevant block
    for box in FigBoxList[3]:
        BoxWeightList.append((box, weights[3]))
    return BoxWeightList
    

def getFigureRectFromMap_Deprecated(denMap, columnROI, c_bias=0, dir=1, dirmargin=0):
    """
    Get the Figure rect from the density map
    
    :param denMap: density map of the figure box
    :param columnROI: ROI of the column
    :param c_bias: critical bias range computation
    :param dir: direction of the density map ([0, 1], i.e. [x, y])
    
    """
    if dir == 1:  # y direction
        up = 3; low = 1; up2 = 2; low2 = 0; dir2 = 0
    elif dir == 0:  # x direction
        up = 2; low = 0; up2 = 3; low2 = 1; dir2 = 1
    FigRects = []
    x_ls = denMap[0]
    ptr_low = 0
    ptr_up = None
    for i in range(len(x_ls)):
        den = denMap[1][i]
        if den > c_bias:
            ptr_up = i
        else:
            if ptr_up is not None:
                FigRects.append((columnROI[low2], x_ls[ptr_low]-dirmargin,
                        columnROI[up2], x_ls[ptr_up]+dirmargin))
                ptr_up = None
            ptr_low = i

    return FigRects


def getFigureRectFromMap(denMap, numBoxList, columnROI, c_bias=3, dir=1, dirmargin=0, boxCenterCriticErr=25):
    """
    Get the equation rect from the density map
    
    :param denMap: density map of the equation box
    :param numBoxList: list of the numbering box
    :param columnROI: ROI of the column
    :param c_bias: critical bias range computation
    :param dir: direction of the density map ([0, 1], i.e. [x, y])
    :param dirmargin: margin in the direction
    """
    if dir == 1:  # y direction
        up = 3; low = 1; up2 = 2; low2 = 0; dir2 = 0
    elif dir == 0:  # x direction
        up = 2; low = 0; up2 = 3; low2 = 1; dir2 = 1
    FigRects = []
    for box in numBoxList:
        center = list(box_center(box))
        if abs(center[dir2]-(columnROI[up2]+columnROI[low2])/2) < boxCenterCriticErr:
            x_ls = denMap[0]
            index0 = int(center[dir]/x_ls[-1]*len(x_ls))
            ptr_up = index0
            ptr_low = index0
            while ptr_up < len(x_ls)-1 and denMap[1][ptr_up] > c_bias:
                ptr_up += 1
            while ptr_low > 0 and denMap[1][ptr_low] > c_bias:
                ptr_low -= 1
            FigRects.append((columnROI[low2], x_ls[ptr_low]-dirmargin,
                            columnROI[up2], x_ls[ptr_up]+dirmargin))
    return FigRects


def getFigRect(page, drawDen=DEBUG_MODE):
    """ Get the figure rect of the page"""
    FigRects = []
    boxLists = getFigBoxList(page)
    FigBoxWeight = getFigBoxWeight(boxLists)
    column_rects = getColumnRectLegacy(page)
    for col in column_rects:
        map = getDensityMap(FigBoxWeight, col, slideavg_windowsize=5)
        if drawDen:
            amp = 40
            maxden = max(map[1]) if max(map[1]) > 0 else 1
            for i in range(len(map[0])-1):
                page.draw_line([col[0]-amp*map[1][i]/maxden, map[0][i]],
                               [col[0]-amp*map[1][i+1]/maxden, map[0][i+1]],
                               color=(0, 1, 0), width=0.5)
        # FigRects += getFigureRectFromMap(map, col)
        FigRects += getFigureRectFromMap(map, boxLists[2], col)
        
    # FIXME: Only support 2 columns
    def get2ColunmDensity(val1, val2):
        if val1*val2 <= 0:
            return min(val1, val2)
        else:
            if val1 > 0:
                return max(val1, val2)
            else:
                return min(val1, val2)
    totalROI = get_bounding_box(column_rects)
    map1 = getDensityMap(FigBoxWeight, column_rects[0], slideavg_windowsize=5)
    map2 = getDensityMap(FigBoxWeight, column_rects[1], slideavg_windowsize=5)
    x_ls = map1[0]
    den = [get2ColunmDensity(map1[1][i], map2[1][i]) for i in range(len(map1[1]))]
    FigRects += getFigureRectFromMap((x_ls, den), boxLists[2], totalROI)
    combine_rect = combineRect(combineRect(FigRects, critic_dis=20, dir=1), critic_dis=0, critic_alignerr=20, dir=0)
    if DEBUG_MODE:
        for rect in combine_rect:
            page.draw_rect(rect, color=(0, 1, 0), width=2)
    return combine_rect


########################
##  PDFFigures 2 API  ##
########################
"""
  <input>
        input PDF(s) or directory containing PDFs
  -i <value> | --dpi <value>
        DPI to save the figures in (default 150)
  -s <value> | --save-stats <value>
        Save the errors and timing information to the given file in JSON fromat
  -t <value> | --threads <value>
        Number of threads to use, 0 means using Scala's default
  -e | --ignore-error
        Don't stop on errors, errors will be logged and also saved in `save-stats` if set     
  -q | --quiet
        Switches logging to INFO level
  -d <value> | --figure-data-prefix <value>
        Save JSON figure data to '<data-prefix><input_filename>.json'
  -c | --save-regionless-captions
        Include captions for which no figure regions were found in the JSON data
  -g <value> | --full-text-prefix <value>
        Save the document and figures into '<full-text-prefix><input_filename>.json
  -m <value> | --figure-prefix <value>
        Save figures as <figure-prefix><input_filename>-<Table|Figure><Name>-<id>.png. `id` will be 1 unless multiple figures are found with the same `Name` in `input_filename`
  -f <value> | --figure-format <value>
        Format to save figures (default png)
"""


def parsePDF_PDFFigures2(pdf_file: str):
    """
    Parse figures from the given scientific PDF using pdffigures2
    """
    args = [
        "java",
        "-jar",
        PDF_FIGURES_JAR_PATH,
        pdf_file,
        "-g",
        op.join(TEMP_DIR, "")
    ]
    _ = subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20
    )
    return json.load(open(op.join(TEMP_DIR, op.basename(pdf_file).replace(".pdf", ".json"))))

        
