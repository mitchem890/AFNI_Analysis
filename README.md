# AFNI_Analysis

*Pipeline is developed by the CCP lab at Washington University St. Louis. *


## Usage

To use the Afni_Analysis pipeline:

1. Download the container `_config.yml`:

    ```yml
    docker pull mitchem890/afni_analysis:latest
    ```

2. Run the subject `Gemfile`:

    ```ruby
    docker run -v /home/mitchell/Desktop/:/mnt mitchem890/afni_analysis:latest --download --origin /mnt --subject 150423 --task Axcpt --wave wave1 --session baseline --destination /mnt --events /mnt --pipeline fmriprep --ncpus 1

    ```

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
