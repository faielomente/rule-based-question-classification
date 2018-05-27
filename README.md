# rule-based-question-classification
A Tagalog question classification algorithm using data mining techniques.

### Manual Setup
Clone the git repository in your machine.
```
git clone git@gitlab.com:modernmachines/icm-api.git
```

Install [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html).
```
sudo pip install virtualenvwrapper
```

Once virtualenvwrapper is installed, add this at the bottom of your shell's rc - `~/.bashrc` or `~/.zshrc`.
```
source /usr/local/bin/virtualenvwrapper.sh
```

To enable virtualenvwrapper in the current shell session, manually invoke the wrapper scripts or your shell's config. You can also
```
# option 1: manually activate virtualenvwrapper for the current shell session
source /usr/local/bin/virtualenvwrapper.sh

# option 2: if you are using bash, manually re-read your bashrc
source ~/.bashrc

# option 2: if you are using zsh, manually re-read your zshrc
source ~/.zshrc
```

Create a virtualenv.
```
mkvirtualenv rule-based-classification --python=python3.6
```

Install the Python dependencies for your development environment.
```
cd /path/to/rule-based-question-classification
pip install -r requirements.txt
```

### POS Tagging
#### Tool:
For the **Part-of-speech** tagging, download the and install [CRF++-0.58](https://taku910.github.io/crfpp/)  
*Note that the ".tar.gz" extension files are for Linux and ".zip" files are for Windows operating systems.*

Extract the downloaded file and navigate to the location of the extracted folder.
```
cd path/to/CRF++-0.58
```

Run the following commands:
```
./configure
make
sudo make install
sudo ldconfig
```

#### Tagging:
Download the [bigram model](https://drive.google.com/file/d/0B8JwvpxiO9EHYk5Nc2oxYTZKWGM/view?usp=sharing)  

Format your data into 7 columns.  
```
WORD ROOT prefix infix suffix reduplication POSTAG
```
*Note: If you don’t have the POStag of your data put XXX instead. Below is the sample format.*   

```
isang   isa _   _   ng  _   JJ-JN
umaga     umaga   _   _   _   _ NN-NNC 
ng  ng  _   _   _   _   PP-OM
disyembre     disyembre   _   _   _   _ NN-NND
,     ,   _   _   _   _ PM-PMC 
ang   ang     _   _   _   _ DT-CDSG
bapor     bapor   _   _   _   _ NN-NNC 
tabo      tabo    _   _   _   _ NN-NNP 
naghahatid    hatid   nag     _   _   ha    VB-IMAF 
ng  ng  _   _   _   _   PP-OM
maraming      dami    ma      _   ng      _ JJ-JCJD 
sakay     sakay   _   _   _   _ NN-NNC 
sa    sa      _   _   _   _ PP-DM
laguna    laguna      _   _   _   _ NN-NNP 
,     ,   _   _   _   _ PM-PMC 
ay    ay      _   _   _   _ LM-LM 
hirap     hirap _     _   _   _ JJ-JCCS 
na    na      _   _   _   _ CC-CCP 
hirap     hirap   _   _   _   _ JJ-JCCS 
sa    sa      _   _   _   _ PP-DM
pagsalunga    salunga     pag     _   _   _ NN-NNC 
sa    sa      _   _   _   _ PP-DM
mabilis   bilis   ma      _   _   _ JJ-JCJD 
na    na      _   _   _   _ CC-CCP 
agos      agos    _   _   _   _ NN-NNC 
ng  ng  _   _   _   _   PP-OM
ilog-Pasig    ilog-Pasig      _   _   _   _ NN-NNP 
.     .   _   _   _   _ PM-PMP
```
*You can use your stemmer to produce the affixes. A sample data file is provided in `pos-tagger/test.txt` as a reference on how to format the POS tagger input file.*  

Sentences must end with proper punctuation. And sentences are separated by a single space. And save it to a file. This file will serve as an input file into the bigram model.

Navigate to your project's directory and run the command below:
```
crf_test -m path/to/bigram.model path/to/test.data -o path/to/output_file_name.out
```
