#import cv2
import glob
import sys

dirpath = 'vgg16'
if len(sys.argv) > 1:
    dirpath = sys.argv[1]

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#font = cv2.FONT_HERSHEY_COMPLEX
#ln = cv2.LINE_AA
files = glob.glob(dirpath + '_sdsel/*.txt')
#img = cv2.imread('title.jpg')
#out = cv2.VideoWriter('{}/single_output.avi'.format(dirpath), fourcc, 25, img.shape[1::-1])
#for i in range(250):
#    out.write(img)

selected = dict()
for fname in files:
    vid_result = [s.strip() for s in open(fname).readlines()]
    vid_name = vid_result[0].split()[1]
    gt_label = vid_result[1].split()[1]
    frame_pred = vid_result[2:]

    fname2 = fname.replace('_sdsel/','_s/')
    vid_result2 = [s.strip() for s in open(fname2).readlines()]
    vid_name2 = vid_result2[0].split()[1]
    gt_label2 = vid_result2[1].split()[1]
    frame_pred2 = vid_result2[2:]
    frame_pred2 = vid_result2[:len(frame_pred)]

    if vid_name != vid_name2:
        print('Video names are not equal!')
        print(fname, vid_name, fname2, vid_name2)
        continue

    if gt_label != gt_label2:
        print('GT labels are not equal!')
        print(fname, vid_name, fname2, vid_name2)
        continue

    nFalseS = sum([gt_label != pred for pred in frame_pred2])
    nFalseSDSEL = sum([gt_label != pred for pred in frame_pred])

    if nFalseS < 2:
        print('Too good result- False Num: {} among {}.'.format(nFalseSDSEL, len(frame_pred)))
        continue
    if nFalseSDSEL > 0.8*len(frame_pred):
        print('Too bad result- False Num: {} among {}.'.format(nFalseSDSEL, len(frame_pred)))
        continue
    if nFalseS < nFalseSDSEL*1.2:
        print('Too similar results - False Num: {} vs {}.'.format(nFalseS, nFalseSDSEL))
        continue

    sid = vid_name[:-3]
    sval = (nFalseS+1.0) / (nFalseSDSEL+1.0)
    if not sid in selected:
        selected[sid] = [fname, sval, vid_name]
    elif selected[sid][1] < sval:
        selected[sid] = [fname, sval, vid_name]

for key, val in sorted(selected.iteritems()):
    print(val[0], val[1], val[2])
#    vid_result = [s.strip() for s in open(fname).readlines()]
#    vid_name = vid_result[0].split()[1]
#    gt_label = vid_result[1].split()[1]
#    frame_pred = vid_result[2:]
#
#    fname2 = fname.replace('_sdsel/','_s/')
#    vid_result2 = [s.strip() for s in open(fname2).readlines()]
#    vid_name2 = vid_result2[0].split()[1]
#    gt_label2 = vid_result2[1].split()[1]
#    frame_pred2 = vid_result2[2:]
#    frame_pred2 = vid_result2[:len(frame_pred)]
#
#    if vid_name != vid_name2:
#        print('Video names are not equal!')
#        print(fname, vid_name, fname2, vid_name2)
#        continue
#
#    if gt_label != gt_label2:
#        print('GT labels are not equal!')
#        print(fname, vid_name, fname2, vid_name2)
#        continue
#
#    nFalseS = sum([gt_label != pred for pred in frame_pred2])
#    nFalseSDSEL = sum([gt_label != pred for pred in frame_pred])
#
#    if nFalseS < 5:
#        print('Too good result- False Num: {} among {}.'.format(nFalseSDSEL, len(frame_pred)))
#        continue
#    if nFalseSDSEL*2 > len(frame_pred):
#        print('Too bad result- False Num: {} among {}.'.format(nFalseSDSEL, len(frame_pred)))
#        continue
#    if nFalseS < nFalseSDSEL*2:
#        print('Too similar results - False Num: {} vs {}.'.format(nFalseS, nFalseSDSEL))
#        continue
#
#    for ind in range(len(frame_pred)):
#        imgname = '/mnt/ssd/tmp/jolee/ch/jpegs_256/{}/frame{:06d}.jpg'.format(vid_name,ind+1)
#        img = cv2.imread(imgname)
#
#        cv2.putText(img, 'GT: {}'.format(gt_label), (10,25), font, 0.5, (255,255,255), 1, ln)
#        if gt_label == frame_pred2[ind]:
#            color = (255,0,0)
#        else:
#            color = (0,0,255)
#        cv2.putText(img, ' S: {}'.format(frame_pred2[ind]), (10,45), font, 0.5, color, 1, ln)
#
#        if gt_label == frame_pred[ind]:
#            color = (255,0,0)
#        else:
#            color = (0,0,255)
#        cv2.putText(img, ' M: {}'.format(frame_pred[ind]), (10,65), font, 0.5, color, 1, ln)
#
#        out.write(img)
#
#out.release()
