**Whisper: Open-Source Audio Transcription and Subtitling Suite**
===============================================
https://whishper.net/

Overview
--------

Whisper is an open-source, locally installed audio transcription and subtitling suite that provides a full-featured web-based user interface. You can access the source code and installation instructions on GitHub at [https://github.com/pluja/whishper](https://github.com/pluja/whishper).

Documentation
------------

For detailed installation guides and documentation, please visit: <https://whishper.net/guides/install/>

### Quick Installation Guide (Linux/MacOS)

#### Step 1: Download the Installation Script
```
curl -fsSL -o get-whishper.sh https://raw.githubusercontent.com/pluja/whishper/main/get-whishper.sh
```

#### Step 2: Run the Installation Script
```
bash get-whishper.sh
```

![image](https://github.com/al-amin/ai-Artificial-Intelligence/assets/2225839/efdff430-fb3f-4232-ac22-659fa5f0896f)

#### Step 3: Run the download Scripts and files [Manual] from https://whishper.net/guides/install/#linux--macos
```
curl -o docker-compose.yml https://raw.githubusercontent.com/pluja/whishper/main/docker-compose.yml && \
 curl -o .env https://raw.githubusercontent.com/pluja/whishper/main/example.env && \
 curl -o nginx.conf https://raw.githubusercontent.com/pluja/whishper/main/nginx.conf
```
![image](https://github.com/al-amin/ai-Artificial-Intelligence/assets/2225839/622d8521-111c-4ed0-bb02-094109291740)

#### Step 4A: if require create the folder again [optional]
```
mkdir ./whishper_data/libretranslate/{data,cache}
```
![image](https://github.com/al-amin/ai-Artificial-Intelligence/assets/2225839/1d007238-4a11-4dcf-81b2-4f9d23cc7431)

#### Step 4B: Give the permission  [change the LOCATION]
```
sudo chmod -R 777 /LOCATION/whishper_web_ui/whishper_data
```
![image](https://github.com/al-amin/ai-Artificial-Intelligence/assets/2225839/eac83471-5ae1-45f0-9aab-b54ed24bbb44)


#### Step 5: run the docker command
```
docker compose up -d
```
![image](https://github.com/al-amin/ai-Artificial-Intelligence/assets/2225839/acbf1a06-bda4-40d3-8886-49f809826e3a)
![image](https://github.com/al-amin/ai-Artificial-Intelligence/assets/2225839/b7cb4a55-7dfe-4bcf-8f80-1d54bf6a98a0)

#### Step 6: Done! You can now access Whishper at http://localhost:8082.
![image](https://github.com/al-amin/ai-Artificial-Intelligence/assets/2225839/40532a86-34cf-4968-acc3-d42ef79a0d54)


Stay Up-to-Date
---------------

To access the latest updates, release notes, and changes, please visit the Whisper GitHub page at [https://github.com/pluja/whishper?tab=readme](https://github.com/pluja/whishper?tab=readme).

Let me know if you need any further modifications!
