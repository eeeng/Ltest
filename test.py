import os
import cv2
import time
import argparse
import posenet
import tensorflow as tf
import matplotlib.pyplot as plt

 

cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

 
model = 101
scale_factor = 0.4
 
with tf.Session() as sess:
    model_cfg, model_outputs = posenet.load_model(model, sess)
    output_stride = model_cfg['output_stride']
    start = time.time()
 
    incnt = 0

    while True:

        incnt += 1
        try:

          input_image, draw_image, output_scale = posenet.read_cap(
                cap, scale_factor=scale_factor, output_stride=output_stride)
        except:
          break

        heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
            model_outputs,
            feed_dict={'image:0': input_image}
        )

        pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multiple_poses(
            heatmaps_result.squeeze(axis=0),
            offsets_result.squeeze(axis=0),
            displacement_fwd_result.squeeze(axis=0),
            displacement_bwd_result.squeeze(axis=0),
            output_stride=output_stride,
            min_pose_score=0.25)

        keypoint_coords *= output_scale

        draw_image = posenet.draw_skel_and_kp(
                draw_image, pose_scores, keypoint_scores, keypoint_coords,
                min_pose_score=0.25, min_part_score=0.25)
        cv2.write(draw_image)

cv2.release()
cap.release()
