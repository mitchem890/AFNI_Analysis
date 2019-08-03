#!/bin/bash

mmp_surface="/home/ramirezc/DMCC_hcp/atlases/HCP-MMP/Glasser_et_al_2016_HCP_MMP1.0_RVVG/HCP_PhaseTwo/Q1-Q6_RelatedValidation210/MNINonLinear/fsaverage_LR32k/Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii"
mmp_volume_222="/home/ramirezc/DMCC_hcp/atlases/HCP-MMP1_on_MNI152_ICBM2009a_nlin_222.nii.gz"
mmp_volume_2p4="/home/ramirezc/DMCC_hcp/atlases/HCP-MMP1_on_MNI152_ICBM2009a_nlin_2p4.nii.gz"

workdir="/home/ramirezc/people/matthew"
hcpdir="/scratch/ramirezc/DMCCPILOT/PREPROC"

subjects="568963"
tasks="Axcpt Cuedts Stern Stroop"
sessions="Bas Pro Rea"
phaseENCS="1_AP 2_PA"

for subject in $subjects; do
    for task in $tasks; do
       for session in $sessions; do
            for phaseE in $phaseENCS; do
            wb_command \
                -cifti-parcellate \
                ${hcpdir}/${subject}/MNINonLinear/Results/tfMRI_${task}${session}${phaseE}/tfMRI_${task}${session}${phaseE}_Atlas.dtseries.nii \
                ${mmp_surface} \
                COLUMN ${workdir}/${subject}_tfMRI_${task}${session}${phaseE}_MMPparc_LR.parc

            wb_command \
                -nifti-information \
                "${workdir}/${subject}_tfMRI_${task}${session}${phaseE}_MMPparc_LR.parc" -print-matrix > "${workdir}/${subject}_tfMRI_${task}${session}${phaseE}_MMPparcSurf_LR_timeseries.txt"
            done # phase encodings
        done # sessions
    done # tasks
done # subjecst




#parc_L=${StudyFolder}/${Subject}/MNINonLinear/fsaverage_LR32k/${Subject}.L.aparc.a2009s.32k_fs_LR.dlabel.nii
#parc_R=${StudyFolder}/${Subject}/MNINonLinear/fsaverage_LR32k/${Subject}.R.aparc.a2009s.32k_fs_LR.dlabel.nii

#wb_command \
#    -cifti-create-label ${StudyFolder}/${Subject}/MNINonLinear/fsaverage_LR32k/${Subject}.L.aparc.a2009s.32k_fs_LR.dlabel.nii  \
#    -left-label ${StudyFolder}/${Subject}/MNINonLinear/fsaverage_LR32k/${Subject}.L.aparc.a2009s.32k_fs_LR.label.gii \
#    -roi-left ${StudyFolder}/${Subject}/MNINonLinear/fsaverage_LR32k/${Subject}.L.atlasroi.32k_fs_LR.shape.gii
