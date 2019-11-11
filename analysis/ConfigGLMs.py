#!/bin/bash
# configModel.sh
#This File will load in the relevent models for all of the glms as well as other information such as force TR and Results directories

#Event Models and Indexes
buttonPressEvents="'TENTzero(0,16.8,8)'"
buttonIDX="0..5"
blockONandOFF="'TENTzero(0,16.8,8)'"

#block (sustained Block-long activity). These are duration Modulated blocks, meaning the durations of the blocks will be modulated based on the Evt files
#The Format of:
#onset:duration onset:duration onset:duration
#onset:duration onset:duration onset:duration
Block="'dmBLOCK(1)'"
#HRF MODEL and index for the events_HRF glm
HRF="'BLOCK(2,1)'"
HRFIDX="0..0"

#Task Events and idx values The idx values should be 0-numOfTents-3 because of the zero index and the 2 poles on each end dont count
AxcptEventTent="'TENTzero(0,21.6,10)'"
AxcptEventIDX="0..7"
CuedtsEventTent="'TENTzero(0,24,11)'"
CuedtsEventIDX="0..8"
SternEventTent="'TENTzero(0,26.4,12)'"
SternEventIDX="0..9"
StroopEventTent="'TENTzero(0,16.8,8)'"
StroopEventIDX="0..5"

#EVENTGLMS These are used in the glm_session Events
AxcptEventRegressors=["block blockONandOFF AX AY Ang BX BY Bng", "block blockONandOFF button1 button2"]
AxcptEventModels = [Block +" "+blockONandOFF+" "+AxcptEventTent+" "+AxcptEventTent+" " + AxcptEventTent+ " " + AxcptEventTent +" " + AxcptEventTent+ " " + AxcptEventTent,
                    Block +" "+blockONandOFF+" "+buttonPressEvents+" "+buttonPressEvents]
AxcptEventGLMLabels=["Cues", "Buttons"]
AxcptEventContrasts=["+0.5*AX[[idx]] +0.5*AY[[idx]] -0.5*BX[[idx]] -0.5*BY[[idx]]", "+0.5*AY[[idx]] +0.5*BX[[idx]] -0.5*AX[[idx]] -0.5*BY[[idx]]", "+0.5*Ang[[idx]] +0.5*Bng[[idx]] -0.25*AX[[idx]] -0.25*AY[[idx]] -0.25*BX[[idx]] -0.25*BY[[idx]]", "+button1[[idx_buttons]] -button2[[idx_buttons]]"]
AxcptEventContrastLabels=["Acue_Bcue", "HI_LO_conf", "Nogo_Go", "B1_B2"]
AxcptEventContrastsGLMids=["Cues", "Cues", "Cues", "Buttons"]
AxcptSingleRegressorConditions=["block", "block", "blockONandOFF", "blockONandOFF", "AX", "AY", "Ang", "BX", "BY", "Bng", "button1", "button2"]
AxcptSingleRegressorGLMids=["Cues", "Buttons", "Cues", "Buttons", "Cues", "Cues", "Cues", "Cues", "Cues", "Cues", "Buttons", "Buttons"]


CuedtsEventRegressors=["block blockONandOFF Inc NoInc", "block blockONandOFF ConInc ConNoInc InConInc InConNoInc", "block blockONandOFF letter number", "block blockONandOFF button1 button2"]
CuedtsEventModels = [Block +" "+blockONandOFF+" "+CuedtsEventTent+" "+CuedtsEventTent,
                    Block +" "+blockONandOFF+" "+CuedtsEventTent+" "+CuedtsEventTent+" "+CuedtsEventTent+" "+CuedtsEventTent,
                    Block +" "+blockONandOFF+" "+CuedtsEventTent + " " + CuedtsEventTent,
                    Block + " " + blockONandOFF+" "+buttonPressEvents+" "+buttonPressEvents]
CuedtsEventGLMLabels=["Incentive", "CongruencyIncentive", "LetterNumber", "Buttons"]
CuedtsEventContrasts=["+Inc[[idx]] -NoInc[[idx]]", "+0.5*ConInc[[idx]] +0.5*InConInc[[idx]] -0.5*ConNoInc[[idx]] -0.5*InConNoInc[[idx]]", "+0.5*InConInc[[idx]] +0.5*InConNoInc[[idx]] -0.5*ConInc[[idx]] -0.5*ConNoInc[[idx]]",  "+letter[[idx]] -number[[idx]]", "+button1[[idx_buttons]] -button2[[idx_buttons]]"]
CuedtsEventContrastLabels=["Inc_NoInc", "Inc_NoInc", "InCon_Con", "Let_Num", "B1_B2"]
CuedtsEventContrastsGLMids=["Incentive", "CongruencyIncentive", "CongruencyIncentive", "LetterNumber", "Buttons"]
CuedtsSingleRegressorConditions=["block", "block", "block", "block", "blockONandOFF", "blockONandOFF", "blockONandOFF", "blockONandOFF", "Inc", "NoInc", "ConInc", "ConNoInc", "InConInc", "InConNoInc", "letter", "number", "button1", "button2"]
CuedtsSingleRegressorGLMids=["Incentive", "CongruencyIncentive", "LetterNumber", "Buttons", "Incentive", "CongruencyIncentive", "LetterNumber", "Buttons", "Incentive", "Incentive", "CongruencyIncentive", "CongruencyIncentive", "CongruencyIncentive", "CongruencyIncentive", "LetterNumber", "LetterNumber", "Buttons", "Buttons"]


SternEventRegressors=["block blockONandOFF LL5NP LL5NN LL5RN not5NP not5NN not5RN", "block blockONandOFF button1 button2"]
SternEventModels = [Block + " " + blockONandOFF + " " + SternEventTent+" "+SternEventTent+" "+SternEventTent+" "+SternEventTent+" "+SternEventTent+" "+SternEventTent,
                    Block + " " + blockONandOFF + " " + buttonPressEvents + " " + buttonPressEvents]
SternEventGLMLabels=["ListLength", "Buttons"]
SternEventContrasts=["+0.5*LL5RN[[idx]] +0.5*not5RN[[idx]] -0.5*LL5NN[[idx]] -0.5*not5NN[[idx]]", "+LL5RN[[idx]] -LL5NN[[idx]]", "+not5RN[[idx]] -not5NN[[idx]]", "+0.33*not5NP[[idx]] +0.33*not5NN[[idx]] +0.33*not5RN[[idx]] -0.33*LL5NP[[idx]] -0.33*LL5NN[[idx]] -0.33*LL5RN[[idx]]", "+button1[[idx_buttons]] -button2[[idx_buttons]]"]
SternEventContrastLabels=["RN_NN_all", "RN_NN_LL5", "RN_NN_not5", "not5_LL5", "B1_B2"]
SternEventContrastsGLMids=["ListLength", "ListLength", "ListLength", "ListLength", "Buttons"]
SternSingleRegressorConditions=["block", "block", "blockONandOFF", "blockONandOFF", "LL5NP", "LL5NN", "LL5RN", "not5NP", "not5NN", "not5RN", "button1", "button2"]
SternSingleRegressorGLMids=["ListLength", "Buttons", "ListLength", "Buttons", "ListLength", "ListLength", "ListLength", "ListLength", "ListLength", "ListLength", "Buttons", "Buttons"]


StroopEventRegressors=["block blockONandOFF PC50Con PC50InCon biasCon biasInCon"]
StroopEventModels = [Block + " " + blockONandOFF + " " + StroopEventTent + " " + StroopEventTent + " " + StroopEventTent + " " + StroopEventTent]
StroopEventGLMLabels=["Congruency"]
StroopEventContrasts=["+biasInCon[[idx]] -biasCon[[idx]]", "+PC50InCon[[idx]] -PC50Con[[idx]]", "+0.5*biasInCon[[idx]] +0.5*PC50InCon[[idx]] -0.5*biasCon[[idx]] -0.5*PC50Con[[idx]]"]
StroopEventContrastLabels=["InCon_Con_bias", "InCon_Con_PC50", "InCon_Con_PC50bias"]
StroopEventContrastsGLMids=["Congruency", "Congruency", "Congruency"]
StroopSingleRegressorModels = [Block + " " + blockONandOFF + " " + HRF + " " + HRF + " " + HRF + " " + HRF]
StroopSingleRegressorConditions=["block", "blockONandOFF", "PC50Con", "PC50InCon", "biasCon", "biasInCon"]
StroopSingleRegressorGLMids = ["Congruency", "Congruency", "Congruency"]

StroopReaSingleRegressorGLMids = ["Congruency", "Congruency", "Congruency"]
StroopReaSingleRegressorConditions=["block", "blockONandOFF", "PC50Con", "PC50InCon", "biasCon", "biasInCon","buffCon"]
StroopReaEventRegressors=["block blockONandOFF PC50Con PC50InCon biasCon biasInCon buffCon"]
StroopReaEventModels = [Block + " " + blockONandOFF + " " + StroopEventTent + " " + StroopEventTent + " "
                        + StroopEventTent + " " + StroopEventTent + " " + StroopEventTent]
StroopReaSingleRegressorModels = [Block + " " + blockONandOFF + " " + HRF + " " + HRF + " " + HRF + " " + HRF + " " + HRF]

#AtlasDirectory and Atlases
Atlas_Dir="/home/atlases"
VolumeAtlasesMB4=["gordon_2p4_resampled_wsubcort_LPI", "communities_2p4_resampled_LPI", "HCP-MMP1_on_MNI152_ICBM2009a_nlin_2p4", "HCP-MMP1_L_on_MNI152_ICBM2009a_nlin_2p4", "HCP-MMP1_R_on_MNI152_ICBM2009a_nlin_2p4", "Schaefer2018_400Parcels_7Networks_order_FSLMNI152_2p4"]
SurfaceAtlasesMB4=["gordon_333", "HCP-MMP_RelatedParcellation210.CorticalAreas_dil_Colors.32k_fs_LR", "Schaefer2018_400Parcels_7Networks_order"]
SubCorticalAtlasesMB4=["gordon_222_resampled_wsubcort_LPI", "Schaefer2018_400Parcels_7Networks_order_FSLMNI152_222"]
SubCorticalAtlasesMatthew=["Schaefer2018_400Parcels_7Networks_order_FSLMNI152_222"]

VolumeAtlasesMB8=["gordon_222_resampled_wsubcort_LPI", "communities_222_resampled_LPI", "HCP-MMP1_on_MNI152_ICBM2009a_nlin_222", "HCP-MMP1_L_on_MNI152_ICBM2009a_nlin_222", "HCP-MMP1_R_on_MNI152_ICBM2009a_nlin_222", "Schaefer2018_400Parcels_7Networks_order_FSLMNI152_222"]
SurfaceAtlasesMB8=["gordon_333", "HCP-MMP_RelatedParcellation210.CorticalAreas_dil_Colors.32k_fs_LR", "Schaefer2018_400Parcels_7Networks_order"]
SubCorticalAtlasesMB8=["gordon_222_resampled_wsubcort_LPI"]

#Atlases for the Fmriprep subjects with fsaverage5 templates
SurfaceAtlasesFS5=["Schaefer2018_400Parcels_7Networks_order_10K"]

#Forced TR values for AFNI. When using Giftis or text files afni isnot able to determine the TR value for them
ForceTRVolumeMB4="FALSE"
ForceTRSurfaceMB4=1.2
ForceTRVolumePreParcellatedMB4=1.2
ForceTRSurfacePreParcellatedMB4=1.2

ForceTRVolumeMB8="FALSE"
ForceTRSurfaceMB8=0.8
ForceTRVolumePreParcellatedMB8=0.8
ForceTRSurfacePreParcellatedMB8=0.8

#Output Directory For each of the analysis Types
VolumeResultsDir="RESULTS"
SurfaceResultsDir="SURFACE_RESULTS"
VolumePreParcellatedResultsDir="PREPARCELLATED_RESULTS"
SurfacePreParcellatedResultsDir="PREPARCELLATED_SURFACE_RESULTS"
SubCorticalPreParcellatedResultsDir="PREPARCELLATED_CIFTI_SUBCORTICAL"