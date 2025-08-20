# Fork Notes
This is my personal attempt at an update to a more recent software stack as the original project seems dead. The original readme with some updates follows.

Tested with Ubuntu 22.04, GNU Radio Companion 3.10.1.1, and Python 3.10.12

I was not able to fix Examples/APRS_RX_RTL.grc. Help is welcome.
# gr-APRS-python3 - A GNU Radio Block for Receiving APRS
GNU Radio Hierarchial Block(s) to Test and Receive APRS Packet (with examples). Tested on GNU Radio v3.7.10 / Linux Ubuntu.

![](./gnuradio_logo.svg)

## Dependency
* **GNU Radio**. Please check out [https://www.gnuradio.org/](https://www.gnuradio.org/) or [Their GitHub repo](https://github.com/gnuradio/gnuradio)

## Installation (Updated for Python3)
This OOT Module is built upon GNU Radio hierarchial block scheme. The hierarchial block itself is "transparently" built graphically / visually using GRC. The hier blocks are provided in the gr-APRS-python3/HierBlock folder.
Installation steps :
* `git clone https://github.com/arglurgl/gr-APRS-python3.git`
* `cd gr-APRS-python3/HierBlock/`
* `gnuradio-companion AFSK_Demod.grc` **AFSK_Demod.grc** should be installed **first**.
* **Click RUN** (F6) button on GNU Radio companion (It will do nothing on the foreground, since it will just build and install the Hier Block silently). Then **Close**.
* Because of a gnuradio bug (https://github.com/gnuradio/gnuradio/issues/5531) check if files `AFSK_Demod.block.yml` and `AFSK_Demod.py` were installed properly to `~/.grc_gnuradio`. If not copy them there manually from `gr-APRS-python3/HierBlock/` via `cp AFSK_Demod.py AFSK_Demod.block.yml ~/.grc_gnuradio/`. If not, the next block will not be runnable.
* `gnuradio-companion APRS_Rx.grc` **APRS_Rx.grc** should be installed **after** AFSK_Demod.grc.
* Again, **Click RUN** (F6) button and then Close.
* Again, check if the new files: `APRS_Rx.block.yml` and `APRS_Rx.py` were installed properly to `~/.grc_gnuradio`. If not copy them there manually from `gr-APRS-python3/HierBlock/` via `cp APRS_Rx.py APRS_Rx.block.yml ~/.grc_gnuradio/`. 
* **Open the GNU Radio companion**. The new Hier Block will be listed under APRS module or possibly under 'no module specified'.

And then **very important** steps :
* determine your python lib folder by running `python3 -m site --user-site`
* output should be something like `/home/user/.local/lib/python3.10/site-packages`
* `cd ..` if you are still in `HierBlock/`
* `cp Module/packet.py /home/user/.local/lib/python3.XY/site-packages/` This will copy **packet.py** files from **gr-APRS-python3/Module/** into **/usr/lib/python3.XY/** directory. Replace XY with what you found in the first step. Without this, the **HDLC to AX.25** block will not run.

Finish, and now you can open grc files on **gr-APRS-python3/Examples/** or **gr-APRS-python3/TestScripts/** and run it.

### About The HDLC to AX.25 block (which is part of the examples)
This block which functions to convert HDLC data into TNC2 APRS formats is constructed from the "Python Block" which native to the GNU Radio Companion. To build one yourself:
* From GNU Radio Core module, under Misc, add Python Block into your flowgraph.
![](./embedded_python_block.png)
* Double Click that block to open the properties and then click Open in Editor. If then you asked about which editor to choose, just select default or any editor you prefer.
* In the editor, copy and paste python code from **gr-APRS-python3/Module/epb.py**, save, close, and hit OK.
* Now your Python Block should be turned into HDLC to AX.25 Block, have message i/o ports which labelled as "hdlc in" and "ax25 out".
* If there is some legacy code left somewhere in the example that I missed this block might break due to old print statements. Simply change e.g.`print e` to `print(e)` in this case by editing the blocks code or recreating it from `epb.py`

![](./hdlc_to_ax25_block.png)

## Hier Blocks
All the hier blocks are constructed graphically using GNU Radio Companion. AFSK Demod hier block is required by the APRS Rx hier block (hier block which contains another hier block within), so it should be installed first.

### AFSK Demod
![](./AFSK_Demod.grc.png)

### APRS Rx
![](./APRS_Rx.grc.png)

## Examples
There are some grc examples included in **gr-APRS-python3/Examples** and **gr-APRS-python3/TestScripts** folder. WAV files are also included in the **gr-APRS-python3/WAV** for testing purposes.

A Few notes:
* AFSK Demod hier block (Filterbank AFSK Demodulator) is recommended to run with input samples per symbol (**integer**) of at least 20 and must be **a value of input sample rate divided by baudrate** (**integer**). For example, at baudrate of 1200baud, if you run at minimum recommended samples per symbol of 20, then the input sample rate must be 24kHz (24kHz / 1200baud = 20 sps).
* The output of the APRS decoder (HDLC to AX25 block) is sent to the **Socket PDU Block**. To examine this output, you can open terminal and run `telnet localhost 52001`. Image below shows the output using terminal, which the transmitted messages are some random strings under experimental data type (`,` data type) for testing purposes.
![](./aprs_output.png)

### APRS RX RTL
From **gr-APRS-python3/Examples/APRS_RX_RTL.grc**. This examples utilizes the low cost RTL SDR dongle for receiving APRS signal on 144.390 Mhz (for usage on another frequency, please change the frequency in the grc).
![](./APRS_RX_RTL.grc.png)

### APRS SCARD
From **gr-APRS-python3/Examples/APRS_SCARD.grc**. This examples utilizes the onboard sound card for the usage with a VHF Radio receiver. Audio from the Radio SPK output should be fed into the MIC input of your soundcard.
![](./APRS_SCARD.grc.png)

### APRS AFSK Complete WAV
From **gr-APRS-python3/TestScripts/APRS_AFSK_Complete_WAV.grc**. This examples will decode AFSK audio files which included in **gr-APRS-python3/WAV**. This example is mainly for testing purposes (for example, to find the best values of Mu and Gain Mu). Make sure to check the sample rate if you use your own files.
![](./APRS_AFSK_Complete_WAV.grc.png)

## TODO
* Bundle up all the codes using gr_modtool
* Optimizing AFSK Demodulation and Clock Sync process
* Tidy up this README file a bit :)

## Acknwoledgement
* [WB2OSZ](https://github.com/wb2osz/direwolf) for which the AFSK Demod scheme is pretty much based on their excellent works.
* [Bob Bruninga](https://github.com/tkuester/gr-bruninga) and
* [Dani Estevez](https://github.com/daniestevez/gr-satellites) for the clock synchronization method.

## Contributing
1. Fork it [https://github.com/handiko/gr-APRS-python3/fork](https://github.com/handiko/gr-APRS-python3/fork)
2. Create new branch (`git checkout -b add-blah-blah`)
3. Do some editing / create new feature
4. Commit your works (`git commit -m "Adding some blah blah blah.."`)
5. Push to the branch (`git push -u origin add-blah-blah`)
6. Create a new Pull Request

.
