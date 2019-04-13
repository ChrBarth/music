#!/usr/bin/env python3

# by Christoph Barth 2019
# a simple script that generates a scale on a given root

# TODO: Chords
# FIXME: some note names are not correct, for example "ees" should be "es" 

# the note names. The second value is their relative distance to c
# so we know when to use flat/sharp notes:
notes     = { 'c': 0,
              'd': 2,
              'e': 4,
              'f': 5,
              'g': 7,
              'a': 9,
              'b':11 }

# define some scales:

# major scale:
major_scale = [ 2, 2, 1, 2, 2, 2, 1 ]
# minor scale:
minor_scale = [ 2, 1, 2, 2, 1, 2, 2 ]
# hungarian minor:
hungarian_minor_scale = [ 2, 1, 3, 1, 1, 3, 1 ]
# minor pentatonic:
minor_pentatonic_scale = [ 0, 3, 2, 2, 0, 3, 2 ]

def distance_from_c(note):
    # calculates the distance from the next lower c for a given note:
    # needed to calculate the distance between two notes
    basenote = note[0]
    basedist = notes[basenote]
    # calculate additional distance for each "is/es":
    stepsup   = note.count("is")
    stepsdown = note.count("es")
    dist = basedist + stepsup - stepsdown
    return dist

def get_scale(intervals, rootnote):
    # intervals is the list (like in major_scale[]) of intervals,
    scale = [rootnote]
    # create a list out of the notes ( [c,d,e,f,g,a,b] ):
    notes_list      = list(notes.keys())
    # get the index of the scale's rootnote:
    notes_index     = notes_list.index(rootnote[0])
    # save the previous index here so we can calculate the distance
    previous_index  = notes_index

    # walk down the intervals:
    for step in intervals:
        octave_skip = False
        notes_index +=  1
        if notes_index >= len(notes):
            notes_index = 0
            octave_skip = True
        note = notes_list[notes_index]

        # calculate the distance between the current note and the previous note
        # and add "is" or "es" if needed:
        dist_from_c      = distance_from_c(note)
        prev_dist_from_c = distance_from_c(scale[-1])
        dist = dist_from_c - prev_dist_from_c
        # are we skipping an octave?
        if octave_skip:
            dist += 12

        if dist > step:
            # distance between current and previous note
            # is too big, so add one or more "es" to the note:
            for i in range(dist-step):
                note = note + "es"
        elif step > dist:
            # distance between current and previous note
            # is too small, so add one or more "is" to the note:
            for i in range(step-dist):
                note = note + "is"

        previous_index  = notes_index
        # for pentatonics:
        if step != 0:
            scale.append(note)
    return scale

if __name__ == "__main__":
    print(get_scale(minor_pentatonic_scale, "fis"))
    print(get_scale(major_scale, "d"))
    print(get_scale(minor_scale, "c"))
    print(get_scale(hungarian_minor_scale, "a"))
