#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 16:30:46 2022

@author: ftan1
"""

import numpy as np
import os 
import pandas as pd


def asnr(img, mask):
    # calculate std and mean
    img_p = img[mask==1] # parenchyma
    img_a = img[mask==2] # aorta
    img_t = img[mask==3] # trachea
    img_b = img[mask==4] # background
        
    # calculate SNR
    p_snr = np.mean(img_p) / np.std(img_b)
    a_snr = np.mean(img_a) / np.std(img_b)
    t_snr = np.mean(img_t) / np.std(img_b)
    #print(np.mean(img_p), np.mean(img_a), np.mean(img_t), np.std(img_b))
    
    return p_snr, a_snr, t_snr

if __name__ == '__main__':
    import seaborn as sns
    img_list = [ 
        '/data/larson4/UTE_Lung/2018-06-05_pat/cfl/P12800',
        '/data/larson4/UTE_Lung/2018-08-08_pat/cfl/P49152',
        '/data/larson4/UTE_Lung/2018-09-05_pat1/cfl/P45568',
        '/data/larson4/UTE_Lung/2018-10-26_pat/cfl/P15872',
        '/data/larson4/UTE_Lung/2019-02-15_pat/cfl/P13312',
        '/data/larson5/UTE_Lung/2019-03-07_pat/cfl/P35840',
        '/data/larson4/UTE_Lung/2019-03-25_pat/cfl/P86528',
        '/data/larson4/UTE_Lung/2019-04-10_pat/cfl/P62464',
        '/data/larson4/UTE_Lung/2019-05-29_pat/cfl/P21504',
        '/data/larson4/UTE_Lung/2020-01-09_pat/cfl/P05120',
        '/data/larson4/UTE_Lung/2021-03-15_pat/cfl/P43008',
        '/data/larson5/UTE_Lung/2021-04-06_pat/cfl/P37888',
        '/data/larson4/UTE_Lung/2021-04-12_pat/cfl/P12800',
        '/data/larson4/UTE_Lung/2021-04-19_pat/cfl/P00512',
        #'/data/larson4/UTE_Lung/2021-11-16_pat/cfl/P71168',
        '/data/larson4/UTE_Lung/2022-04-21_pat/cfl',
        '/data/larson4/UTE_Lung/2022-04-22_pat/cfl/P15872',
        '/data/larson4/UTE_Lung/2022-05-20_pat/cfl/P31232',
        ]
    
    mask_list = [ 
        '/data/larson4/UTE_Lung/2018-06-05_pat/seg/P12800',
        '/data/larson4/UTE_Lung/2018-08-08_pat/seg/P49152',
        '/data/larson4/UTE_Lung/2018-09-05_pat1/seg/P45568',
        '/data/larson4/UTE_Lung/2018-10-26_pat/seg/P15872',
        '/data/larson4/UTE_Lung/2019-02-15_pat/seg/P13312',
        '/data/larson5/UTE_Lung/2019-03-07_pat/seg/P35840',
        '/data/larson4/UTE_Lung/2019-03-25_pat/seg/P86528',
        '/data/larson4/UTE_Lung/2019-04-10_pat/seg/P62464',
        '/data/larson4/UTE_Lung/2019-05-29_pat/seg/P21504',
        '/data/larson4/UTE_Lung/2020-01-09_pat/seg/P05120',
        '/data/larson4/UTE_Lung/2021-03-15_pat/seg/P43008',
        '/data/larson5/UTE_Lung/2021-04-06_pat/seg/P37888',
        '/data/larson4/UTE_Lung/2021-04-12_pat/seg/P12800',
        '/data/larson4/UTE_Lung/2021-04-19_pat/seg/P00512',
        #'/data/larson4/UTE_Lung/2021-11-16_pat/seg/P71168',
        '/data/larson4/UTE_Lung/2022-04-21_pat/seg',
        '/data/larson4/UTE_Lung/2022-04-22_pat/seg/P15872',
        '/data/larson4/UTE_Lung/2022-05-20_pat/seg/P31232',
        ]
    
    SNR = []
    for mask_dir, img_dir in zip(mask_list, img_list):
        # load mask 
        #mask_dict = loadmat(os.path.join(mask_dir, 'mask_roi.mat'))
        #mask = mask_dict['mask_3D']
        mask  = np.load(os.path.join(mask_dir, 'mask_roi.npy'))
        
        # load image
        n_ref = 3
        snr_ls = [] 
        for img_file in ['xdgrasp.npy', 'mostmoco.npy', 'mocolor_vent.npy']:
        
            # load image
            img = np.abs(np.load(os.path.join(img_dir, img_file)))
            img = img[n_ref,:,:,:]
            img = img / np.amax(img)
            
            # calculate apparent SNR
            p_snr, a_snr, t_snr = asnr(img, mask)
            snr_ls.extend([p_snr, a_snr, t_snr])
            
        SNR.append(snr_ls)
    
    #%% 
    # SNR bar plot/ box plot for xd grasp, mocolor, mocolor vent
    A = np.repeat(['XD Recon', 'MostMoCo', 'MoCoLoR'], 3)
    B = np.array(['parenchyma', 'aorta', 'trachea'] * 3)
    snr_df = pd.DataFrame(SNR, columns = pd.MultiIndex.from_tuples(zip(A,B)))
    s_d = snr_df.describe()
    snr_df = snr_df.melt(var_name = ['Recon Method','Tissue'], value_name = 'SNR')
    
    # ax = sns.boxplot(data=snr_df, hue = 'Recon Method', y = 'SNR', x = 'Tissue', palette='muted')
    # from statannotations.Annotator import Annotator
    # pairs=[[("parenchyma", "XD Recon"), ("parenchyma","MoCoLoR")], 
    #        [("parenchyma", "XD Recon"), ("parenchyma","iMoCoLoR")],
    #        [("aorta", "XD Recon"), ("aorta","MoCoLoR")], 
    #        [("aorta", "XD Recon"), ("aorta","iMoCoLoR")],
    #        [("trachea", "XD Recon"), ("trachea","MoCoLoR")], 
    #        [("trachea", "XD Recon"), ("trachea","iMoCoLoR")],
    #        [("parenchyma", "MoCoLoR"), ("parenchyma","iMoCoLoR")],
    #        [("aorta", "MoCoLoR"), ("aorta","iMoCoLoR")],
    #        [("trachea", "MoCoLoR"), ("trachea","iMoCoLoR")],
    #        ]
    # annotator = Annotator(ax, pairs, data=snr_df, hue = 'Recon Method', y = 'SNR', x = 'Tissue', palette='muted')
    # annotator.configure(test='t-test_paired', text_format='star').apply_and_annotate()
    sns.set_theme(context='talk')
    #snr_df1 = snr_df[snr_df['Recon Method']!="MoCoLoR"] # using only imocolor
    plt.figure(figsize=(20,6), dpi=300)
    g = sns.catplot(data=snr_df, kind='box', x = 'Recon Method', y = 'SNR', col = 'Tissue', palette='muted', sharey=False)
    from statannotations.Annotator import Annotator
    #pairs=[("XD Recon", "LoR") , ("XD Recon", "MoCoLoR"), ("XD Recon", "iMoCoLoR"), ("LoR", "MoCoLoR"), ("LoR", "iMoCoLoR"), ("MoCoLoR","iMoCoLoR")]
    pairs=[("XD Recon", "MostMoCo") , ("XD Recon", "MoCoLoR"),  ("MostMoCo", "MoCoLoR")]
    
    annotator = Annotator(g.axes[0,0], pairs, data=snr_df[snr_df['Tissue']=="parenchyma"], x = 'Recon Method', y = 'SNR', palette='muted')
    annotator.configure(test='t-test_paired', text_format='star').apply_and_annotate()
    
    annotator = Annotator(g.axes[0,1], pairs, data=snr_df[snr_df['Tissue']=="aorta"], x = 'Recon Method', y = 'SNR', palette='muted')
    annotator.configure(test='t-test_paired', text_format='star').apply_and_annotate()

    annotator = Annotator(g.axes[0,2], pairs, data=snr_df[snr_df['Tissue']=="trachea"], x = 'Recon Method', y = 'SNR', palette='muted')
    annotator.configure(test='t-test_paired', text_format='star').apply_and_annotate()
    
    g.savefig('/working/larson2/ftan/imoco_recon/figures/snr_md/SNR.eps')