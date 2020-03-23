# This File will load in the relevent models for all of the glms as well as other information such as force TR and Results directories

# AtlasDirectory and Atlases
Atlas_Dir = "/home/Atlases"
VolumeAtlasesMB4 = ["gordon_2p4_resampled_wsubcort_LPI", "communities_2p4_resampled_LPI",
                    "HCP-MMP1_on_MNI152_ICBM2009a_nlin_2p4", "HCP-MMP1_L_on_MNI152_ICBM2009a_nlin_2p4",
                    "HCP-MMP1_R_on_MNI152_ICBM2009a_nlin_2p4", "Schaefer2018_400Parcels_7Networks_order_FSLMNI152_2p4"]
SurfaceAtlasesMB4 = ["gordon_333", "HCP-MMP_RelatedParcellation210.CorticalAreas_dil_Colors.32k_fs_LR",
                     "Schaefer2018_400Parcels_7Networks_order"]
SubCorticalAtlasesMB4 = ["gordon_222_resampled_wsubcort_LPI", "Schaefer2018_400Parcels_7Networks_order_FSLMNI152_222"]
SubCorticalAtlasesMatthew = ["Schaefer2018_400Parcels_7Networks_order_FSLMNI152_222"]

VolumeAtlasesMB8 = ["gordon_222_resampled_wsubcort_LPI", "communities_222_resampled_LPI",
                    "HCP-MMP1_on_MNI152_ICBM2009a_nlin_222", "HCP-MMP1_L_on_MNI152_ICBM2009a_nlin_222",
                    "HCP-MMP1_R_on_MNI152_ICBM2009a_nlin_222", "Schaefer2018_400Parcels_7Networks_order_FSLMNI152_222"]
SurfaceAtlasesMB8 = ["gordon_333", "HCP-MMP_RelatedParcellation210.CorticalAreas_dil_Colors.32k_fs_LR",
                     "Schaefer2018_400Parcels_7Networks_order"]
SubCorticalAtlasesMB8 = ["gordon_222_resampled_wsubcort_LPI"]

# Atlases for the Fmriprep subjects with fsaverage5 templates
SurfaceAtlasesFS5 = ["Schaefer2018_400Parcels_7Networks_order_10K"]

# Forced TR values for AFNI. When using Giftis or text files afni isnot able to determine the TR value for them
ForceTRVolumeMB4 = "FALSE"
ForceTRSurfaceMB4 = 1.2
ForceTRVolumePreParcellatedMB4 = 1.2
ForceTRSurfacePreParcellatedMB4 = 1.2

ForceTRVolumeMB8 = "FALSE"
ForceTRSurfaceMB8 = 0.8
ForceTRVolumePreParcellatedMB8 = 0.8
ForceTRSurfacePreParcellatedMB8 = 0.8

# Output Directory For each of the analysis Types
VolumeResultsDir = "RESULTS"
SurfaceResultsDir = "SURFACE_RESULTS"
VolumePreParcellatedResultsDir = "PREPARCELLATED_RESULTS"
SurfacePreParcellatedResultsDir = "PREPARCELLATED_SURFACE_RESULTS"
SubCorticalPreParcellatedResultsDir = "PREPARCELLATED_CIFTI_SUBCORTICAL"