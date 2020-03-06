# ALICIA
> Don't worry about a THING, mister. My name is ALICIA and you're in good hands with me. (Alicia Masters)

**ALICIA** is a wearable device that can leverage the power of AI at the Edge to transform visual input from the camera into audible description of the environment, providing navigation aid and details to visually impaired people.

## FUNCTIONALITY (expected for final project)
Once powered, **ALICIA** will start up in the background and will wait for a vocal command ("Alicia, describe view") to start to process the environment.
Once an initial description is provided ("TV in front left, chair one in front, table in front, chair two in front, bed on right") the application will provide an update only if the scene changes, new objects detected or an object changes the position relative to the camera. There will be threshold between large (navigable) objects and smaller objects. For example, in the initial description you will hear the table, but probably not all the objects that are on the table.
At this point, the user can ask more details about an object ("Alicia, more details on chair one") or ask for more detailed search to find small objects too ("Alicia, describe more"). Vocal commands can be added to pause the description and perform other tasks.
A fail-back set of push-buttons will be added to provide non-vocal commands.

## FUNCTIONALITY (current version)
For current version **ALICIA** have to be started manually (testing) and provide a vocal (also text) description of the objects found in the environment.

## HARDWARE
**ALICIA** works on a **RaspberryPi 3 B+** (RSP) powered from a power bank and connecting to a **RaspberryPi camera** (a usb camera should work fine too, but the code should be adapted for it).
The Edge AI is processed in an attached **Intel NCS2** usb stick.
Voice input and output is provided through an in-ear piece (both wired and BT headsets should work just fine)

## SOFTWARE
On RaspberryPi I run **Raspbian Buster** with **OpenVino toolkit** (2020.1) for Raspberry and Python3.
If you want to train / optimize your models I recommend (as Intel does too) to use a more powerful computer  to install OpenVino on it and move the optimized IR model to RSP afterwards.
For text-to-speak I used **espeak** (probably will be changed because is a little buggy)
The vocal commands are not implemented yet.

### A note about the models used
With minimum changes to the code (classes labels and output format) **ALICIA** should be able to work with different models from OpenVino models zoo or models trained by yourself.
The initial choice for a testing model was **semantic-segmentation-adas-0001** (mostly because was already optimized) but due to some technical incompatibilities with NCS2 I decided to optimize a more generic model - *ssd_mobilnet_v2_coco* 

Note to note: in order to work on NSC2, the model should be optimized for **FP16** and with the flag **--generate_deprecated_IR_V7** due to some errors in processing v10 IR in NSC2

The command to generate the optimized model is:
> python3 /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json --data_type FP16 --generate_deprecated_IR_V7


## TODO
- improve and optimize the model
- improve TTS 
- add voice commands
- add different levels of detection and "on-demand" levels of details
- create a branch for the case a usb camera is used (use cv.CaptureVideo)
- improve wearability

## Disclaimers
I chose to name the project  ALICIA after Alicia Masters (Alicia Masters is a fictional character appearing in comic books published by Marvel Comics.) 
https://en.wikipedia.org/wiki/Alicia_Masters
All the rights over Alicia Masters name and character are owned by Marvel.