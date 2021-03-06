# AFNI_Analysis

*This pipeline is developed by the Cognitive Control & Psychopathology Laboratory at Washington University St. Louis to replicate the standard analysis processing used on subjects in the Dual Mechanisms of Cognitive Control Study*



## Installation
First you will want to Download the container using either singularity or docker

#### Download the container using docker:

    docker pull ccplabwustl/afni_analysis:latest
   
#### Download the container using singularity:

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
It will be easier if I use an example to explain things. 
The example shows the command to download and run the baseline session of subject 150423 through the entire analysis pipeline

```
singularity run \
-B /my/desired/output/location/:/mnt \
-B /where/my/fmriprep/data/lives:/data:ro \
afni_analysis.simg \
--download \
--wave wave1 \
--subject 150423 \
--session baseline \
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

#### Bind Points `-B`
 
This is called a bind point. singularity containers are an isolated system so the need to be given explicit direction of where they can read and write to your system. in this example I would have a local file location called: 
`/where/my/fmriprep/data/lives`
and I'm binding it to a point in the container called:
`/data`
the `ro` means read only because we wont be writing anything to that directory, 
we want to tell singularity that we don't care if we don't have write permission
The other bind point I'm using is `/my/desired/output/location/:/mnt`
This tell singularity to put the output in the `/mnt` location.


#### Origin `--origin` 
This is where your derivatives folder is for fmriprep. This should be relative to the bind path set above.

#### Destination `--destination`
This is where you want your output to live. This should be relative to the bind path set above 

#### Wave `--wave`
This sets the wave number to look for in the fmriprep location. This if for file naming/finding purposes only.
Currently for the DMCC project the only options available are `wave1` and `wave2`

#### Subject `--subject`
This tells the system which subjects you wish to process. 

#### Session `--session` 
This sets the sessions you want to process. Multiple sessions should be space seperated.
`--session baseline proactive reactive` 

#### Task `--task` 
This sets the tasks that you wish to process. Multiple sessions should be space seperated.
`--task Axcpt Cuedts Stern Stroop`

#### Preanalysis `--preanalysis` 
Is telling your pipeline that you want to run preanalysis. The only reason you wouldn't want to use this is if you've already ran preanalysis previously so you want to skip that stage.

#### Analysis `--analysis`
Is telling the pipeline that you want to run the analysis part of the pipeline (GLMs, ROISTATS) The onlyreason not to include this is if you want to run your own analysis on the afni-ized input data.

#### Volume `--volume` 
This tells the pipeline to run the volume analysis 

#### Surface `--surface` 
This tells the pipeline to run the surface analysis

#### Events `--events` 
This should point to a folder containing your event files. It expects to find a folder with the structure `/mnt/Event_Files/[subject]/evts`
so in the example above. the program expects to find a folder called `/mnt/Event_Files`

#### Pipeline `--pipeline` 
this should be set to `fmriprep` if you are running fmriprep data and `hcp` if you re running data pushed through the hcp preprocessing pipeline

#### NCPUs `--ncpus` 
This sets the number of threads that you want running simultaneously usually i would suggest using a range from 1-12 the max that the pipeline is able to run simutaneously is 12 because we have 4 tasks X 3 sessions

#### Download `--download` 
This tells the pipeline to Download the specified subject from OpenNeuro in the `--origin` location

#### Aux_Analysis `--aux_analysis`
This will tell the pipeline to run your own custom analysis after completing the standard pipline.
This should point to a folder containing all of your bash scripts. This parameter takes more explaination
`--aux_analysis /mnt/MyScripts`

After you have made your file save it and run!
It takes about 6 hours to run a complete subject on ccplinux1 running all 12 threads at once, but if you just want to test a single task in a session for your local machine. That should take much less time.


## Aux_Analysis
In order to make a better gradient from testing analysis from bash scripts to full production. We've implemented a way to do auxiliary analysis with the afni_analysis container.

### What does this mean:
With a few edits of your bash script you can have it running inside the container. Making it easier to run mid-level test (before full on production, and after playing around with it on a few subjects), while still allowing for the benefits of having a locked down environment.

### What is needed:
Inorder to run this aux_analysis you will need to Create a folder in a mountable location.
In that folder you will have your bash scripts that you want to use, along with a .yaml file that will act as an orchestra maestro for your scripts.

#### How the heck do I write a yaml file:
you can check out the file attached as an example.
But basically you will be laying out threads
Each thread has three defining attributes:
   
thread_name: This will just to show you during runtime which thread is running
   
log_file: This will be written to the aux_analysis directory this will basically log every       command that is ran inside of the scripts, as well as a date time.
   
scripts: This is a list of all of the scripts that you want to run inside of the aux_analysis folder. They will run in the order that they are listed

Your yaml file should always be named Aux_Analysis.yaml

### What Changes do I need to make to my scripts:
1.) Change the paths to be relative to what the container will see
If you are pointing to a file in your script the container must be able to see that file and it must be in a path relative to what the container sees.
so if your original script has something like:
```
3dinfo /data/nil-bluearc/ccp-hcp/DMCC_ALL_BACKUPS/HCP_SUBJECTS_BACKUPS/fMRIPrep_AFNI_ANALYSIS/132017/INPUT_DATA/Axcpt/baseline/lpi_scale_blur4_tfMRI_AxcptBas1_AP.nii.gz
```
You will want to have a path bound in the singularity call like:
```
singularity run \
-B /data/nil-bluearc/ccp-hcp/DMCC_ALL_BACKUPS/HCP_SUBJECTS_BACKUPS/fMRIPrep_AFNI_ANALYSIS/:/mnt \
/data/nil-bluearc/ccp-hcp/afni_analysis_aux.simg
```
then you will want to change your command to:
```
3dinfo /mnt/132017/INPUT_DATA/Axcpt/baseline/lpi_scale_blur4_tfMRI_AxcptBas1_AP.nii.gz
```
2.) Make sure you are only using standard functionality for bash, afni, wb-command, or fsl
So some commands wont work if they are not default installs on linux
We could install more things if need be but I would like to avoid that. If you cant figure out a way around this you can ask Nick Bloom or Me to help you figure out a way around if all else fails we can install it on the container.

3.) Your scripts cannot be interactive
You should make it so that there are no external variables to your scripts. as you wont be able to pass variables to and from them at runtime

4.) You will have access to user defined variables
The user defined parameters are available as environment variables

```
echo "This is my --origin $origin"
echo "This is my --subject $subjects"
echo "This is my --wave $wave"
echo "This is my --task parameter $tasks"
echo "This is my --session $sessions"
echo "This is my --destination $destination"
echo "This is my --events $events"
echo "This is my --run_volume $run_volume"
echo "This is my --run_surface $run_surface"
echo "This is my --run_analysis $run_analysis"
echo "This is my --run_preanalysis $run_preanalysis"
echo "This is my --pipeline $pipeline"
echo "This is my --ncpus $ncpus"
echo "This is my --aux_analysis $aux_analysis"
```

All of the environment variables will be in string format when called in the shell
If a variable has multiple parameters like '--sessions baseline proactive reactive'
the parameters will be returned as one string that is space separated.
this should allow you to do loops easier:

```
for session in ${sessions}; do
    echo ${session}
done
```

And you container call should look something like this:
```
singularity run \
-B /data/nil-bluearc/ccp-hcp/DMCC_ALL_BACKUPS/HCP_SUBJECTS_BACKUPS/fMRIPrep_AFNI_ANALYSIS/:/mnt \
-B /data/nil-bluearc/ccp-hcp/DMCC_ALL_BACKUPS/HCP_SUBJECTS_BACKUPS/fMRIPrep_PREPROCESSED/${subject}:/data:ro \
/data/nil-bluearc/ccp-hcp/afni_analysis_aux.simg \
--wave wave1 \
--subject 132017 \
--session baseline proactive reactive \
--task Axcpt Cuedts Stern Stroop \
--origin /data/derivatives/fmriprep/ \
--destination /mnt \
--events /mnt/evts/DMCC2 \
--pipeline fmriprep \
--aux_analysis /mnt/MyScripts \
--ncpus 12
```

### Note:
So far this has only been tested in a limited scenario. I'm up for suggestions if you have any. Also please let me know if you have any questions while you are trying it out.

