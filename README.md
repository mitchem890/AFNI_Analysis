# AFNI_Analysis

*Pipeline is developed by the CCP lab at Washington University St. Louis. *


## Installation
First you will want to Download the container using either singularity or docker

###Download the container using docker:

    ```bash
    docker pull mitchem890/afni_analysis:latest
    ```
###Download the container using singularity:

    ```bash
    singularity build afni_analysis.simg docker://ccplabwustl/afni_analysis:latest
    ```

##Usage

### Parameters

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
