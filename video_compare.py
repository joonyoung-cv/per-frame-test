import cv2
import glob
import sys

dirpath = 'vgg16'
if len(sys.argv) > 1:
	dirpath = sys.argv[1]

files = glob.glob(dirpath + '_sdsel/*.txt')

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

	if nFalseS < 5:
		print('Too good result- False Num: {} among {}.'.format(nFalseSDSEL, len(frame_pred)))
		continue
	if nFalseSDSEL*2 > len(frame_pred):
		print('Too bad result- False Num: {} among {}.'.format(nFalseSDSEL, len(frame_pred)))
		continue
	if nFalseS < nFalseSDSEL*2:
		print('Too similar results - False Num: {} vs {}.'.format(nFalseS, nFalseSDSEL))
		continue

	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	font = cv2.FONT_HERSHEY_SIMPLEX
	ln = cv2.LINE_AA
	for ind in range(len(frame_pred)):
		imgname = '/mnt/ssd/tmp/jolee/ch/jpegs_256/{}/frame{:06d}.jpg'.format(vid_name,ind+1)
		img = cv2.imread(imgname)
		if ind == 0:
			out = cv2.VideoWriter('{}/{}_output.avi'.format(dirpath, vid_name), fourcc, 25, img.shape[1::-1])

		cv2.putText(img, 'GT: {}'.format(gt_label), (10,25), font, 0.5, (255,255,255), 1, ln)
		if gt_label == frame_pred2[ind]:
			color = (255,0,0)
		else:
			color = (0,0,255)
		cv2.putText(img, ' S: {}'.format(frame_pred2[ind]), (10,45), font, 0.5, color, 1, ln)

		if gt_label == frame_pred[ind]:
			color = (255,0,0)
		else:
			color = (0,0,255)
		cv2.putText(img, ' M: {}'.format(frame_pred[ind]), (10,65), font, 0.5, color, 1, ln)

		out.write(img)

	out.release()
