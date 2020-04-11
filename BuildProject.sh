#Use this Docker Image to build a good base for you Docker recipt you can add things to this
#To add in more functionality
docker run --rm kaczmarj/neurodocker:master generate docker \
	--base ubuntu:16.04 --pkg-manager apt \
	--afni version=latest method=binaries \
	--fsl version=5.0.10 \
	--miniconda create_env=neuro \
		conda_install='python=3.6 numpy pandas traits' \
		pip_install='nipype pydeface' \
	--miniconda use_env=neuro \
		conda_install='jupyter' > Dockerfile




#install workbench
echo "RUN mkdir /src && cd /src && wget https://www.humanconnectome.org/storage/app/media/workbench/workbench-linux64-v1.4.1.zip && cd /opt && unzip /src/workbench-linux64-v1.4.1.zip">>Dockerfile
echo "COPY analysis /home/analysis/" >> Dockerfile


#I have the Atlases stored in a git largefilesystem(lfs) this allows for them to hopefully not need to be 
#uploaded each time that you change something in the package
#one of the issues with this is that I am changing the permissions on the /home/Atlases directory which essecntially doubles the size of the layer.
#I couldnt find a quick solution but it shoudl be changed in the future if you find something to work
#But right now it shoudl drastically reduce the time to test and upload new code
echo "RUN apt-get update && \
apt-get upgrade -y && \
apt-get install -y git && curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash && \
sudo apt-get install git-lfs && \
git lfs install" >> Dockerfile
echo "RUN cd /home/ && \
git lfs clone https://github.com/mitchem890/Atlases" >> Dockerfile
echo "ENV PATH=\"/opt/workbench/bin_linux64:\$PATH\"" >> Dockerfile
echo "ENV PATH /opt/miniconda-latest/envs/neuro/bin:\$PATH" >> Dockerfile
echo "ENTRYPOINT [\"python\",\"-u\",\"/home/analysis/run.py\"]" >> Dockerfile
echo "ENV HOME=/home" >> Dockerfile
echo "COPY .afnirc /home" >> Dockerfile
echo "RUN mkdir /testing" >> Dockerfile
echo "RUN mkdir /mnt" >> Dockerfile
sed -i 's/apt-get/apt-get -y/g' Dockerfile
sed -i 's/nlibxmu-headers/libxmu-headers/g' Dockerfile
sed -i 's/nmesa-common-dev/mesa-common-dev/g' Dockerfile
sed -i '/libmng1/d' Dockerfile

docker build --tag afni_analysis .
