import Surface_GLMs
import Volume_GLMs
import roistats

encodings = ['AP', 'PA']
runNums = ['1', '2']
hemispheres = ['L','R']

#This Section Includes all the GLMs and roistats

def analysis(destination, wave, subject, session, task, pipeline, run_volume, run_surface):
        if run_volume:
            Volume_GLMs.event_glms(destination, subject, task, session)
            Volume_GLMs.block_glms(destination, subject, task, session)
            Volume_GLMs.mixed_glms(destination, subject, task, session)
            Volume_GLMs.single_regressor_glm(destination, subject, task, session)
            roistats.block_roistats(subject=subject, task=task, session=session, mb="4", data_dir=destination,
                                    censor=True)
            roistats.contrast_roistats(subject=subject, task=task, session=session, mb="4", data_dir=destination,
                                        censor=True)
            roistats.mixed_roistats(subject=subject, task=task, session=session, mb="4", data_dir=destination,
                                    censor=True)
            roistats.single_regressors_roistats(subject=subject, task=task, session=session, mb="4",
                                                data_dir=destination, censor=True)
            roistats.single_regressors_HRF_roistats(subject=subject, task=task, session=session, mb="4",
                                                    data_dir=destination, censor=True)
            roistats.contrast_HRF_roistats(subject=subject, task=task, session=session, mb="4", data_dir=destination,
                                           censor=True)

        if run_surface:
            for hemisphere in hemispheres:
                Surface_GLMs.block_glms(destination, subject, task, session, hemisphere)
                Surface_GLMs.mixed_glms(destination, subject, task, session, hemisphere)
                Surface_GLMs.single_regressor_glm(destination, subject, task, session, hemisphere)
                Surface_GLMs.event_glms(destination, subject, task, session, hemisphere)

                if pipeline == "fmriprep":
                    fsaverage5 = True
                else:
                    fsaverage5 = False
                roistats.block_roistats_Surface(subject=subject, task=task, session=session,
                                                hemisphere=hemisphere, mb="4", data_dir=destination,
                                                censor=True, fsaverage5=fsaverage5)
                roistats.contrast_roistats_Surface(subject=subject, task=task, session=session,
                                                   hemisphere=hemisphere, mb="4", data_dir=destination,
                                                   censor=True, fsaverage5=fsaverage5)
                roistats.mixed_roistats_Surface(subject=subject, task=task, session=session,
                                                hemisphere=hemisphere, mb="4", data_dir=destination,
                                                censor=True, fsaverage5=fsaverage5)
                roistats.single_regressors_roistats_Surface(subject=subject, task=task, session=session,
                                                            hemisphere=hemisphere, mb="4", data_dir=destination,
                                                            censor=True, fsaverage5=fsaverage5)
                roistats.single_regressors_HRF_roistats_Surface(subject=subject, task=task, session=session,
                                                                hemisphere=hemisphere, mb="4", data_dir=destination,
                                                                censor=True, fsaverage5=fsaverage5)
                roistats.contrast_HRF_roistats_Surface(subject=subject, task=task, session=session,
                                                       hemisphere=hemisphere, mb="4", data_dir=destination,
                                                       censor=True, fsaverage5=fsaverage5)
