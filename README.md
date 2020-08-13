# AFNI_Analysis

*Pipeline is developed by the CCP lab at Washington University St. Louis. *



## Installation
First you will want to Download the container using either singularity or docker

###Download the container using docker:

    docker pull mitchem890/afni_analysis:latest
   
###Download the container using singularity:

    singularity build afni_analysis.simg docker://ccplabwustl/afni_analysis:latest

This will create a singularity image name afni_analysis.simg in the location you are currently in.

##Usage

In order to run the container you'll probably want to create a bash file to make setting the parameters easier.
Open your favorite text editor and paste the following in.
 
### Parameters

     singularity run \
     -B /my/desired/output/location/:/mnt \
     -B /where/my/fmriprep/data/lives:/data:ro \
afni_analysis.simg \
--wave wave1 \
--subject 132017 \
--session baseline proactive reactive \
--task Axcpt Cuedts Stern Stroop \
--origin /data/132017/derivatives/fmriprep/ \
--destination /mnt \
--preanalysis \
--analysis \
--volume \
--surface \
--events /mnt/Event_Files \
--pipeline fmriprep \
--ncpus 12






Then you will want to edit the parameters as needed.

explanation of parameters:
-B
This is called a bind point. singularity containers are an isolated system so the need to be given explicit direction of where they can read and write to your system. in this example I would have a local file location called: 
/where/my/fmriprep/data/lives
and I'm binding it to a point in the container called /data.
the 'ro' means read only because we wont be writing anything to that directory, 
we want to tell singularity that we don't care if we don't have write permission
The other bind point I'm using is /my/desired/output/location/:/mnt
This tell singularity to put the output in that location.

--wave sets the wave number to look for in the fmriprep location this if for file naming/finding purposes only.
--subject is the subject number you want to process
--session are the sessions you want to process. Multiple sessions should be space seperated.
--task are the tasks that you wish to process. Multiple sessions should be space seperated.
--origin is where your derivatives folder is for fmriprep. This should be relative to the bind path set above.
--destination is where you want your output to live. This should be relative to the bind path set above 
--preanalysis is telling your pipeline that you want to run preanalysis. The only reason you wouldn't want to use this is if you've already ran preanalysis previously so you want to skip that stage.
--analysis is telling the pipeline that you want to run the analysis part of the pipeline (GLMs, ROISTATS) The onlyreason not to include this is if you want to run your own analysis on the afni-ized input data.
--volume tells the pipeline to run the volume analysis 
--surface tells the pipeline to run the surface analysis
--events this should point to a folder containing your event files. it expects to find a folder with the structure /mnt/Event_Files/[subject]/evts
so in the example above. the program expects to find a folder called /mnt/Event_Files
--pipeline this should be set to 'fmriprep' if you are running fmriprep data and 'hcp' if you re running data pushed through the hcp preprocessing pipeline
--ncpus this set the number of threads that you want running simultaneously usually i would suggest using a range from 1-12 the max that the pipeline is able to run simutaneously is 12 because we have 4 tasks X 3 sessions

After you have made your file save it and run!
It takes about 6 hours to run a complete subject on ccplinux1 running all 12 threads at once, but if you just want to test a single task in a session for your local machine. That should take much less time.



Docker Instructions

Things you will need:
Docker https://docs.docker.com/
DMCC data processed through fmriprep

Download and install docker for your machine. 

Run The container:

In order to run the container you'll probably want to create a bash file to make setting the parameters easier 
Open your favorite text editor and paste the following in.

docker run -it \
--mount type=bind,source=/my/desired/output/location/,target=/mnt \
--mount type=bind,source=/where/my/fmriprep/data/lives,target=/data,readonly \
ccplabwustl/afni_analysis \
--wave wave1 \
--subject 132017 \
--session baseline proactive reactive \
--task Axcpt Cuedts Stern Stroop \
--origin /data/132017/derivatives/fmriprep/ \
--destination /mnt \
--preanalysis \
--analysis \
--volume \
--surface \
--events /mnt/Event_Files \
--pipeline fmriprep \
--ncpus 12

Then you will want to edit the parameters as needed.

explanation of parameters:
--mount
This is called a bind point. singularity containers are an isolated system so the need to be given explicit direction of where they can read and write to your system. in this example I would have a local file location called: 
/where/my/fmriprep/data/lives
and I'm binding it to a point in the container called /data.
the 'ro' means read only because we wont be writing anything to that directory, 
we want to tell singularity that we don't care if we don't have write permission
The other bind point I'm using is /my/desired/output/location/:/mnt
This tell singularity to put the output in that location.

--wave sets the wave number to look for in the fmriprep location this if for file naming/finding purposes only.
--subject is the subject number you want to process
--session are the sessions you want to process. Multiple sessions should be space seperated.
--task are the tasks that you wish to process. Multiple sessions should be space seperated.
--origin is where your derivatives folder is for fmriprep. This should be relative to the bind path set above.
--destination is where you want your output to live. This should be relative to the bind path set above 
--preanalysis is telling your pipeline that you want to run preanalysis. The only reason you wouldn't want to use this is if you've already ran preanalysis previously so you want to skip that stage.
--analysis is telling the pipeline that you want to run the analysis part of the pipeline (GLMs, ROISTATS) The onlyreason not to include this is if you want to run your own analysis on the afni-ized input data.
--volume tells the pipeline to run the volume analysis 
--surface tells the pipeline to run the surface analysis
--events this should point to a folder containing your event files. it expects to find a folder with the structure /mnt/Event_Files/[subject]/evts
so in the example above. the program expects to find a folder called /mnt/Event_Files
--pipeline this should be set to 'fmriprep' if you are running fmriprep data and 'hcp' if you re running data pushed through the hcp preprocessing pipeline
--ncpus this set the number of threads that you want running simultaneously usually i would suggest using a range from 1-12 the max that the pipeline is able to run simutaneously is 12 because we have 4 tasks X 3 sessions

After you have made your file save it and run!
It takes about 6 hours to run a complete subject on ccplinux1 running all 12 threads at once, but if you just want to test a single task in a session for your local machine. That should take much less time.

Slate will respect the following variables, if set in your site's `_config.yml`:

```yml
title: [The title of your site]
description: [A short description of your site's purpose]
```

Additionally, you may choose to set the following optional variables:

```yml
show_downloads: ["true" or "false" to indicate whether to provide a download URL]
google_analytics: [Your Google Analytics tracking ID]
```
