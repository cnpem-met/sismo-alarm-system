## Seismometer/accelerometer alarm system

Implementation of scripts that sends alerts when some predefined limits of vibration were reached.

This piece of software was used during the soil compaction of the NB4 laboratory beside Sirius, with the purposes of warning potentially dangerous vibration reaching optical components of Carnaúba and Cateretê beamlines and also to keep track of the steamroller movimentation.

To do so, both an e-mail notifying system and a EPICS IOC PV updating scheme were implemented in independent modules based on threads. 