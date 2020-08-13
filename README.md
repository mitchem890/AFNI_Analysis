# AFNI_Analysis

*This pipeline is developed by the Cognitive Control & Psychopathology Laboratory at Washington University St. Louis to replicate the standard analysis processing used on subjects in the Dual Mechanisms of Cognitive Control Study*



## Installation
First you will want to Download the container using either singularity or docker

###Download the container using docker:

    docker pull mitchem890/afni_analysis:latest
   
###Download the container using singularity:

    singularity build afni_analysis.simg docker://ccplabwustl/afni_analysis:latest

This will create a singularity image name afni_analysis.simg in the location you are currently in.

## Usage

In order to run the container you'll probably want to create a bash file to make setting the parameters easier.
Open your favorite text editor and paste the following in.

```
singularity run \
[-B /local/bind/point:/mnt [-B /other/local/bind/point:/data:ro]] \
afni_analysis.simg \
[--download]
--wave [wave] \
--subject [SUBJECT [SUBJECT]] \
--session [SESSION[SESSION]] \
--task [TASK [TASK]] \
--origin [ORIGIN_DIR] \
--destination [DESTINATION_DIR] \
[--preanalysis] \
[--analysis] \
[--volume] \
[--surface] \
--events [EVENTS_DIR] \
--pipeline [PIPELINE] \
--ncpus [NCPUS]
[--aux_analysis AUX_ANALYSIS_DIR]
```

Then you will want to edit the parameters as needed.

### Parameters:
This is an indepth explaination of the parameters that you will be using to run the container.
It will be easier if I use an example
```singularity run \
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
```

#### Bind Points
 `-B`
 
This is called a bind point. singularity containers are an isolated system so the need to be given explicit direction of where they can read and write to your system. in this example I would have a local file location called: 
`/where/my/fmriprep/data/lives`
and I'm binding it to a point in the container called:
`/data`
the `ro` means read only because we wont be writing anything to that directory, 
we want to tell singularity that we don't care if we don't have write permission
The other bind point I'm using is `/my/desired/output/location/:/mnt`
This tell singularity to put the output in the `/mnt` location.


#### Origin
`--origin` 
This is where your derivatives folder is for fmriprep. This should be relative to the bind path set above.

#### Destination
`--destination`
This is where you want your output to live. This should be relative to the bind path set above 

#### Wave
`--wave`
This sets the wave number to look for in the fmriprep location. This if for file naming/finding purposes only.
Currently for the DMCC project the only options available are `wave1` and `wave2`

#### Subject
`--subject`
This tells the system which subjects you wish to process. 

#### Session
`--session` 
This sets the sessions you want to process. Multiple sessions should be space seperated.
`--session baseline proactive reactive` 

#### Task
`--task` 
This sets the tasks that you wish to process. Multiple sessions should be space seperated.
`--task Axcpt Cuedts Stern Stroop`

#### Preanalysis
`--preanalysis` 
Is telling your pipeline that you want to run preanalysis. The only reason you wouldn't want to use this is if you've already ran preanalysis previously so you want to skip that stage.

#### Analysis
`--analysis`
Is telling the pipeline that you want to run the analysis part of the pipeline (GLMs, ROISTATS) The onlyreason not to include this is if you want to run your own analysis on the afni-ized input data.

#### Volume
`--volume` 
This tells the pipeline to run the volume analysis 

#### Surface
`--surface` 
This tells the pipeline to run the surface analysis

#### Events
`--events` 
This should point to a folder containing your event files. It expects to find a folder with the structure `/mnt/Event_Files/[subject]/evts`
so in the example above. the program expects to find a folder called `/mnt/Event_Files`

#### Pipeline
`--pipeline` 
this should be set to `fmriprep` if you are running fmriprep data and `hcp` if you re running data pushed through the hcp preprocessing pipeline

#### NCPUs
`--ncpus` 
This sets the number of threads that you want running simultaneously usually i would suggest using a range from 1-12 the max that the pipeline is able to run simutaneously is 12 because we have 4 tasks X 3 sessions


#### Download
`--download` 
This tells the pipeline to Download the specified subject from OpenNeuro in the `--origin` location


#### Aux_Analysis
`--aux_analysis`
This will tell the pipeline to run your own custom analysis after completing the standard pipline.
This should point to a folder containing all of your bash scripts. This parameter takes more explaination
`--aux_analysis /mnt/MyScripts`


After you have made your file save it and run!
It takes about 6 hours to run a complete subject on ccplinux1 running all 12 threads at once, but if you just want to test a single task in a session for your local machine. That should take much less time.
