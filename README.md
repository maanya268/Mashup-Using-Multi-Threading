
# Mashup
Mashup performs the following tasks:

1) Download N videos of X singer from “Youtube” [N can be any positive number and X can be any singer e.g. sharry maan]
2) Convert all the videos to audio
3) Cut first Y sec audios from all downloaded files [Y can be any positive number]
4) Merge all audios to make a single output file (use pypi.org)

#### Run the program through command line as:
```
Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>

Example: python 102003366.py “Sharry Maan” 20 20 102003366-output.mp3
```

### Multi-Threading
This project has been created using the concept of multi-threading.

Multi-threading is a programming concept that allows multiple threads of execution to run concurrently within a single process. A thread is a separate path of execution within a program that can perform a specific task independently of other threads. By using multi-threading, a program can utilize the resources of a CPU more efficiently and can perform multiple tasks simultaneously.

Multiple threads have been created to faster the process of downloading.

Multi-Treading reduced the process time significantly.

### Screenshots
Terminal:
![image](https://user-images.githubusercontent.com/74601983/224363398-42ee09a2-b5fb-4851-82ae-cdb4f9846b53.png)

Folder is created on desktop containing the final mashedup audio file.
![image](https://user-images.githubusercontent.com/74601983/224363982-8af93aeb-1a1e-4c61-ac41-0bf78f27b7f7.png)

Video Folder:
![image](https://user-images.githubusercontent.com/74601983/224363707-1e7b38bd-93d4-4e29-847c-4cf21c588426.png)

Audio Folder:
![image](https://user-images.githubusercontent.com/74601983/224363601-f03f0e95-18a6-453c-b3ed-f5f3d07aea1e.png)

Folder made after cutting the audios:
![image](https://user-images.githubusercontent.com/74601983/224363840-fbe35261-4739-48c2-89b9-088bfb600b05.png)

Output file:
![image](https://user-images.githubusercontent.com/74601983/224364489-660bf4cd-3509-4013-afaa-28ee80faa738.png)

### Applications

Mashup could be used in various applications such as:

Music Production: This could be used by music producers to 
create new remixes or mashups of popular songs by a specific artist. They could download multiple videos of the artist from Youtube, extract the audio, and then use the cut and merge features to create a new, unique audio file.
 
Podcasting: Podcasters could use this to create a highlight reel of interviews or discussions they have had with a particular guest.

Entertainment Industry: This could also be used in the entertainment industry to create promotional material for upcoming concerts or events.
