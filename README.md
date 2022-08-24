# eiger2cbf-spawn
Script for spawning the eiger2cbf frame conversion utility for windows over multiple processes, speeding it up and avoiding a bug where the utility writes blank frames

There are two different versions, both are spawned by running:
python eiger2cbf-spawnX.py [Master h5 file] [number of processes to use] [output file stem] [OPTIONAL test]

If the final parameter (test) is specified, the script will test [number of processes] +-5 for 10 frames each, and tell how fast they are.

Version two will split the available frames into the appropriate number of pools, and kick off that many processes.
Version three will fire off each frame individually, using the specified number of pools. This can avoid problems with individual frames not being written correctly.
