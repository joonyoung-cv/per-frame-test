import cv2
import glob

dirpath = 'vggm'

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

	if vid_name != vid_name2:
		print('Video names are not equal!')
		print(fname, vid_name, fname2, vid_name2)
		continue

	if gt_label != gt_label2:
		print('GT labels are not equal!')
		print(fname, vid_name, fname2, vid_name2)
		continue


	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	font = cv2.FONT_HERSHEY_SIMPLEX
	ln = cv2.LINE_AA
	for ind in range(len(frame_pred)):
		imgname = '/mnt/ssd/tmp/jolee/ch/jpegs_256/{}/frame{:06d}.jpg'.format(vid_name,ind+1)
		img = cv2.imread(imgname)
		if ind == 0:
			out = cv2.VideoWriter('{}/{}_output.avi'.format(dirpath, vid_name), fourcc, 25, img.shape[1::-1])

		cv2.putText(img, 'GT: {}'.format(gt_label), (10,20), font, 0.5, (255,255,255), 1, ln)
		if gt_label == frame_pred2[ind]:
			color = (255,255,255)
		else:
			color = (0,0,255)
		cv2.putText(img, ' S: {}'.format(frame_pred2[ind]), (10,40), font, 0.5, color, 1, ln)

		if gt_label == frame_pred[ind]:
			color = (255,255,255)
		else:
			color = (0,0,255)
		cv2.putText(img, ' M: {}'.format(frame_pred[ind]), (10,60), font, 0.5, color, 1, ln)

		out.write(img)

	out.release()
