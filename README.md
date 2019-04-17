# CS188 and CSCE580 reversed submission_autograder.py 

CS188 Intro to AI is a course provided for free by UC Berkeley for use by other institutions. It is also in use at the University of South Carolina as CSCE580.

## Getting Started

These instructions will get you a copy of the program up and running on your local machine. See "Installing" for notes on what is required to run this on a live system.

### Installing

Clone and cd into the directory

```
$ git clone https://github.com/brokencodebank/Berkeley-CS188-UofSC-CSCE580.git
$ cd Berkeley-CS188-UofSC-CSCE580
```

The only weird package required is a python3 specific fork of a package called primefac

```
$ pip3 install git+git://github.com/elliptic-shiho/primefac-fork@master
```

Then you simply need to run the program

```
$ python3 submission_autograder_encryption_reversed.py 
-------------------------------------------------------------------------------

CS 188 Local Submission Autograder Tool
-------------------------------------------------------------------------------

usage: submission_autograder_encryption_reversed.py [-h] [--encrypt]
                                                    [--decrypt] [--modify]
                                                    [--genkeys] [--size SIZE]
                                                    [--crackkey]
                                                    [--printcsce580key] [-n N]
                                                    [-p P] [-q Q] [-e E]
                                                    [-d D]

optional arguments:
  -h, --help         show this help message and exit
  --encrypt          Encrypts a reinforcement.plaintext.token
  --decrypt          Decrypts a reinforcement.token
  --modify           Modifies a reinforcement.plaintext.token
  --genkeys          Generates private and public keys for encryption
  --size SIZE        The size of the keys to generate
  --crackkey         Attempts to factor and then recover a private key from a
                     public key
  --printcsce580key  Prints the public key that was found in the csce580
                     reinforcement assignment
  -n N               n component of public and private key
  -p P               p component of the private key
  -q Q               q component of the private key
  -e E               e component of public key
  -d D               d component of private key
```

## Notes on Key Strength

The key found within the obfuscated CSCE 580 submission_autograder.py was found to be very short and weak. It can be retrieved as shown below:

```
$ python3 submission_autograder_encryption_reversed.py --printcsce580key
-------------------------------------------------------------------------------

CS 188 Local Submission Autograder Tool
-------------------------------------------------------------------------------

Key found in obfuscated file: -e 33751518165820762234153612797743228623 -n 56285023496349038954935919614579038707
```

If you want to crack it you can easily do this with `--crackkey` as shown:

```
$ python3 submission_autograder_encryption_reversed.py --crackkey -e 33751518165820762234153612797743228623 -n 56285023496349038954935919614579038707
-------------------------------------------------------------------------------

CS 188 Local Submission Autograder Tool
-------------------------------------------------------------------------------

 Crack key: -e 33751518165820762234153612797743228623 -n 56285023496349038954935919614579038707

Cracking Public_Key....................................................... DONE

 Private Key found: -d 36786304852261144029274009415324198959 -p 6480256949166153253 -q 8685616008419467319
```

If you are a professor or TA for another class based on these tools then you should use a much stronger key! I provide a function for generating a significantly better key that can be included in the program without much problem. Run it with `--genkeys`. By default it will create a 2048 bit key which is much better for this task.

DO NOT USE THESE KEYS THIS IS JUST AN EXAMPLE

```
$ python3 submission_autograder_encryption_reversed.py --genkeys
-------------------------------------------------------------------------------

CS 188 Local Submission Autograder Tool
-------------------------------------------------------------------------------

Generating keys of size: 2048............................................. DONE

 Generated Keys:

 Private_Key: -d 11777646818189557037170692783343828249185976674860675697981225511684329356541181199734717744444158582229447050353437374461486405115990871123706633377607282799600489937709780267821366570195552502876432588302917697820261235869984154331218196971163331837044162399831352588399476621874040511577017871194591135882133762248033463060845129267539669890432067788799031660590676376111495066817152857080418934368933974868772556474304272392320365130025697444044249989973643491791152570647551618869351701686993496375750734693129150978979342893401076699043783896599665846313187026230222236896009991980598883235022974683723366542337 -p 175568442352164289159475769601710579547542445668006085101325859263705909706392432173679228993696911871934104929504878632055288858414838527527941536861378543309713980904708144472504215711537616476808097424517030055062388514580781400424390811787581727576542317775399277199999068910735531181535059361691647254017 -q 151815133976452480267888387325105576320262952289485352490626775123627553504622670359910575663563522373683986190495179598765911916863026972367882125815118028984210128370352250692598452496982012468190610162516068370348683275524651244847111028850246311808303339614120068575187227169182139662026219308306547917623
 Public_Key: -e 65537 -n 26653946597730895388136872576470336405500927288246973418232521024871573363708670613177740834201347456872518779619918685385629149213947087980743866558522341684361245521174276370461994575465517606996538642204783216341947602307094565503126730028631212355549683041463702288958061375315411202293691778876339627484266759122769069430728073325294071434338968997340140629212214302995332779278412001407149516723865838816727143009101170139916810759272275990255574054364837796836096353569704217321969358130840592099029437224921325495039484207827949431943433372508828438909253894485070806096806754121718458528692004587577471841591

```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
