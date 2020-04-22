#Use this Docker Image to build a good base for you Docker recipt you can add things to this
#To add in more functionality
docker run --rm repronim/neurodocker:0.7.0 \
	generate docker \
	--base neurodebian:stretch \
	--pkg-manager apt \
	--install connectome-workbench \
	--afni version=latest method=binaries \
	--miniconda create_env=neuro \
	conda_install='python=3.6 numpy pandas traits' \
	--miniconda use_env=neuro \
	conda_install='jupyter' > Dockerfile




echo "COPY analysis /home/analysis/" >> Dockerfile


#I have the Atlases stored in a git largefilesystem(lfs) this allows for them to hopefully not need to be 
#uploaded each time that you change something in the package
#one of the issues with this is that I am changing the permissions on the /home/Atlases directory which essecntially doubles the size of the layer.
#I couldnt find a quick solution but it shoudl be changed in the future if you find something to work
#But right now it shoudl drastically reduce the time to test and upload new code
echo "RUN apt-get update && \
apt-get upgrade -y && \
apt-get install -y git && \
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \ 
apt-get install git-lfs && \
git lfs install" >> Dockerfile
#Get the atlases
echo "RUN cd /home/ && \
git lfs clone https://github.com/mitchem890/Atlases && \
chmod 777 -R /home/Atlases" >> Dockerfile

#Add Python to path
echo "ENV PATH /opt/miniconda-latest/envs/neuro/bin:\$PATH" >> Dockerfile
#Set entry point to the program
echo "ENTRYPOINT [\"python\",\"-u\",\"/home/analysis/run.py\"]" >> Dockerfile
#Add $HOME variable
echo "ENV HOME=/home" >> Dockerfile
echo "RUN mkdir /testing" >> Dockerfile
echo "RUN mkdir /data" >> Dockerfile
#Copy the afnirc to a findable location
echo "COPY .afnirc /home" >> Dockerfile

docker build --tag afni_analysis .
