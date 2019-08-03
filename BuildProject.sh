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



#RUN apt-get update
#RUN apt-get -y install build-essential
#RUN apt-get -y install build-essential g++
#RUN apt-get install -y qtbase5-dev
#RUN apt-get install -y qtdeclarative5-dev
#RUN apt install gpgv

#install workbench
echo "RUN mkdir /src && cd /src && wget https://www.humanconnectome.org/storage/app/media/workbench/workbench-linux64-v1.3.2.zip && cd /opt && unzip /src/workbench-linux64-v1.3.2.zip">>Dockerfile
echo "COPY analysis /home/" >> Dockerfile 
echo "ENV PATH=\"/opt/workbench/bin_linux64:\$PATH\"" >> Dockerfile
echo "ENV PATH /opt/miniconda-latest/envs/neuro/bin:\$PATH" >> Dockerfile
echo "ENTRYPOINT [\"python\",\"-u\",\"/home/Run_Analysis.py\"]" >> Dockerfile
sed -i 's/apt-get/apt-get -y/g' Dockerfile
sed -i 's/nlibxmu-headers/libxmu-headers/g' Dockerfile
sed -i 's/nmesa-common-dev/mesa-common-dev/g' Dockerfile
sed -i '/libmng1/d' Dockerfile

docker build --tag afni_analysis .
