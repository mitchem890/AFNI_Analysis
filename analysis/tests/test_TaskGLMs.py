import unittest
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from ..classes import Images
from ..classes import TaskGLMs

image1 = Images.hcp_preprocessed_image(
    file='/mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/tfMRI_StroopPro1_AP.nii.gz', wave='wave1',
    subject='346945', session='proactive', task='Stroop', pipeline='hcp', testMode=True)
image2 = Images.hcp_preprocessed_image(
    file='/mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/tfMRI_StroopPro2_PA.nii.gz', wave='wave1',
    subject='346945', session='proactive', task='Stroop', pipeline='hcp', testMode=True)
Stroop_Images = [image1, image2]

image1= Images.hcp_preprocessed_image(
    file='/mnt/afni_container_output/346945/INPUT_DATA/Axcpt/baseline/tfMRI_AxcptBas1_AP.nii.gz', wave='wave1',
    subject='346945', session='baseline', task='Axcpt', pipeline='hcp', testMode=True)
image2 = Images.hcp_preprocessed_image(
    file='/mnt/afni_container_output/346945/INPUT_DATA/Axcpt/baseline/tfMRI_AxcptBas2_PA.nii.gz', wave='wave1',
    subject='346945', session='baseline', task='Axcpt', pipeline='hcp', testMode=True)
Axcpt_Images = [image1, image2]


image1 = Images.hcp_preprocessed_image(
    file='/mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/tfMRI_StroopPro1_AP.nii.gz', wave='wave1',
    subject='346945', session='proactive', task='Stern', pipeline='hcp', testMode=True)
image2 = Images.hcp_preprocessed_image(
    file='/mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/tfMRI_StroopPro2_PA.nii.gz', wave='wave1',
    subject='346945', session='proactive', task='Stern', pipeline='hcp', testMode=True)
Stern_Images = [image1, image2]

image1= Images.hcp_preprocessed_image(
    file='/mnt/afni_container_output/346945/INPUT_DATA/Axcpt/baseline/tfMRI_AxcptBas1_AP.nii.gz', wave='wave1',
    subject='346945', session='baseline', task='Cuedts', pipeline='hcp', testMode=True)
image2 = Images.hcp_preprocessed_image(
    file='/mnt/afni_container_output/346945/INPUT_DATA/Axcpt/baseline/tfMRI_AxcptBas2_PA.nii.gz', wave='wave1',
    subject='346945', session='baseline', task='Cuedts', pipeline='hcp', testMode=True)
Cuedts_Images = [image1, image2]


def print_all_glms():
    StroopGLMs = TaskGLMs.StroopGLMs('/mnt/afni_container_output/', images=Stroop_Images)
    SternGLMs = TaskGLMs.StroopGLMs('/mnt/afni_container_output/', images=Stern_Images)
    CuedtsGLMs = TaskGLMs.StroopGLMs('/mnt/afni_container_output/', images=Cuedts_Images)
    AxcptGLMs = TaskGLMs.StroopGLMs('/mnt/afni_container_output/', images=Axcpt_Images)
    Tasks=[StroopGLMs, SternGLMs, CuedtsGLMs, AxcptGLMs]
    for task in Tasks:
        for type in task.glms:
            for glm in type:
                print(glm.deconvolve.command)
                print(glm.remlfit.command)
                print()

print_all_glms()

class TestStroop_GLMs(unittest.TestCase):


    def test_congruency_event_deconvolve_volume(self):
        output = f"""3dDeconvolve \\
-local_times \\
-x1D_stop \\
-GOFORIT 5 \\
-input '/mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/lpi_scale_blur4_tfMRI_StroopPro1_AP.nii.gz /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/lpi_scale_blur4_tfMRI_StroopPro2_PA.nii.gz' \\
-polort A \\
-float \\
-censor /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/movregs_FD_mask.txt \\
-num_stimts 6 \\
-stim_times_AM1 1 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_block.txt 'dmBLOCK(1)' -stim_label 1 block \\
-stim_times 2 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_blockONandOFF.txt 'TENTzero(0,16.8,8)' -stim_label 2 blockONandOFF \\
-stim_times 3 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_PC50Con.txt 'TENTzero(0,16.8,8)' -stim_label 3 PC50Con \\
-stim_times 4 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_PC50InCon.txt 'TENTzero(0,16.8,8)' -stim_label 4 PC50InCon \\
-stim_times 5 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_biasCon.txt 'TENTzero(0,16.8,8)' -stim_label 5 biasCon \\
-stim_times 6 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_biasInCon.txt 'TENTzero(0,16.8,8)' -stim_label 6 biasInCon \\
-ortvec /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/motion_demean_proactive.1D movregs \\
-x1D X.xmat.1D \\
-xjpeg X.jpg \\
-nobucket"""

        self.maxDiff = None
        self.assertEqual(output, TaskGLMs.StroopGLMs('/mnt/afni_container_output/', images=Stroop_Images)
                         .glms[2][0].deconvolve.command)

    def test_congruency_event_remlfit_volume(self):
        output = """3dREMLfit \\
-matrix X.xmat.1D \\
-GOFORIT 5 \\
-input '/mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/lpi_scale_blur4_tfMRI_StroopPro1_AP.nii.gz /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/lpi_scale_blur4_tfMRI_StroopPro2_PA.nii.gz' \\
-Rvar stats_var_346945_REML.nii.gz \\
-Rbuck STATS_346945_REML.nii.gz \\
-fout \\
-tout \\
-nobout \\
-verb"""
        self.maxDiff = None
        self.assertEqual(output,
                         TaskGLMs.StroopGLMs('/mnt/afni_container_output/', images=Stroop_Images).glms[0][
                             0].remlfit.command)

    def test_congruency_event_deconvolve_surface_L(self):
        output = f"""3dDeconvolve \\
-local_times \\
-x1D_stop \\
-GOFORIT 5 \\
-force_TR 1.2 \\
-input '/mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/lpi_scale_tfMRI_StroopPro1_AP_L.func.gii /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/lpi_scale_tfMRI_StroopPro2_PA_L.func.gii' \\
-polort A \\
-float \\
-censor /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/movregs_FD_mask.txt \\
-num_stimts 6 \\
-stim_times_AM1 1 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_block.txt 'dmBLOCK(1)' -stim_label 1 block \\
-stim_times 2 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_blockONandOFF.txt 'TENTzero(0,16.8,8)' -stim_label 2 blockONandOFF \\
-stim_times 3 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_PC50Con.txt 'TENTzero(0,16.8,8)' -stim_label 3 PC50Con \\
-stim_times 4 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_PC50InCon.txt 'TENTzero(0,16.8,8)' -stim_label 4 PC50InCon \\
-stim_times 5 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_biasCon.txt 'TENTzero(0,16.8,8)' -stim_label 5 biasCon \\
-stim_times 6 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_biasInCon.txt 'TENTzero(0,16.8,8)' -stim_label 6 biasInCon \\
-ortvec /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/motion_demean_proactive.1D movregs \\
-x1D X.xmat_L.1D \\
-xjpeg X_L.jpg \\
-nobucket"""

        self.maxDiff = None
        self.assertEqual(output, TaskGLMs.StroopGLMs('/mnt/afni_container_output/', images=Stroop_Images)
                         .glms[2][1].deconvolve.command)

    def test_congruency_event_remlfit_surface_L(self):
        output = """3dREMLfit \\
-matrix X.xmat_L.1D \\
-GOFORIT 5 \\
-input '/mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/lpi_scale_tfMRI_StroopPro1_AP_L.func.gii /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/lpi_scale_tfMRI_StroopPro2_PA_L.func.gii' \\
-Rvar stats_var_346945_REML_L.func.gii \\
-Rbuck STATS_346945_REML_L.func.gii \\
-fout \\
-tout \\
-nobout \\
-verb"""
        #print(TaskGLMs.AxcptGLMs('/mnt/afni_container_output/', images=Axcpt_Images).glms[4][1].deconvolve.command)
        #print(TaskGLMs.AxcptGLMs('/mnt/afni_container_output/', images=Axcpt_Images).glms[4][1].remlfit.command)

        self.maxDiff = None
        self.assertEqual(output,
                         TaskGLMs.AxcptGLMs('/mnt/afni_container_output/', images=Stroop_Images).glms[1][1].remlfit.command)

    def test_congruency_hrf_event_deconvolve_volume(self):
        output = f"""3dDeconvolve \\
-local_times \\
-x1D_stop \\
-GOFORIT 5 \\
-input '/mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/lpi_scale_blur4_tfMRI_StroopPro1_AP.nii.gz /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/lpi_scale_blur4_tfMRI_StroopPro2_PA.nii.gz' \\
-polort A \\
-float \\
-censor /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/movregs_FD_mask.txt \\
-num_stimts 6 \\
-stim_times_AM1 1 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_block.txt 'dmBLOCK(1)' -stim_label 1 block \\
-stim_times 2 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_blockONandOFF.txt 'TENTzero(0,16.8,8)' -stim_label 2 blockONandOFF \\
-stim_times 3 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_PC50Con.txt 'BLOCK(2,1)' -stim_label 3 PC50Con \\
-stim_times 4 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_PC50InCon.txt 'BLOCK(2,1)' -stim_label 4 PC50InCon \\
-stim_times 5 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_biasCon.txt 'BLOCK(2,1)' -stim_label 5 biasCon \\
-stim_times 6 /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/346945_Stroop_proactive_biasInCon.txt 'BLOCK(2,1)' -stim_label 6 biasInCon \\
-ortvec /mnt/afni_container_output/346945/INPUT_DATA/Stroop/proactive/motion_demean_proactive.1D movregs \\
-x1D X.xmat.1D \\
-xjpeg X.jpg \\
-nobucket"""

        self.maxDiff = None
        self.assertEqual(output,
                         TaskGLMs.StroopGLMs('/mnt/afni_container_output/', images=Stroop_Images).glms[5][
                             0].deconvolve.command)


suite = unittest.TestLoader().loadTestsFromTestCase(TestStroop_GLMs)
unittest.TextTestRunner(verbosity=2).run(suite)


class TestStroop_Roistats(unittest.TestCase):
    def test_on_blocks_roistats_volume(self):
        output = f'''bash /home/analysis/BashScripts/Roistats.sh \\
-i /mnt/afni_container_output/346945/RESULTS/Stroop/proactive_ON_BLOCKS_censored/STATS_346945_REML.nii.gz \\
-n ON_BLOCKS \\
-w /mnt/afni_container_output/346945/RESULTS/Stroop/proactive_ON_BLOCKS_censored \\
-a /home/Atlases/gordon_2p4_resampled_wsubcort_LPI \\
-r ".nii.gz" \\
-b Coef \\
-f 346945_timecourses_proactive_ON_BLOCKS_Coef_blocks_gordon_2p4_resampled_wsubcort_LPI.txt'''

        self.maxDiff = None
        self.assertEqual(output, TaskGLMs.StroopGLMs('/mnt/afni_container_output/', images=Stroop_Images)
                         .glms[0][0].roistats[0].roistats.command)


suite = unittest.TestLoader().loadTestsFromTestCase(TestStroop_Roistats)
unittest.TextTestRunner(verbosity=2).run(suite)
