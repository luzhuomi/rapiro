Rapiro firmware
===============
##The difference between default sample firmware and  this firmware. 
 1. Motion No. is 2 digits #Mnn. (evilbluechickens-san ) 
 2. Added Servo off command #H. (evilbluechickens-san )
 3. Added Read Analog port #An. n is 6 or 7.
 4. Added Version Info #V. Response is #Ver00.
 5. Motion data moved to Flash. Some motions can be added.
 6. User trim data was separated into include file.

|       |default | This |
|-------|-------|------|
|STOP   | #M0   | #M00 |
|Foward | #M1   | #M01 |
|Back   | #M2   | #M02 |
|Left   | #M4   | #M04 |
|Right  | #M3   | #M03 |
|OFF    | -     | #H   |
|Analog | -     | #A6  |
|C      | #C    | #C   |
|Q      | #Q    | #Q   |
|5      | #M5   | #M05 |
|M6     | #M6   | #M06 |
|M7     | #M7   | #M07 |
|M8     | #M8   | #M08 |
|M9     | #M9   | #M09 |
|M10    | -     | #M10 |
