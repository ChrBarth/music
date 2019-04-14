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

# chords:
# (they are different, since we need to store 2 things:
# the interval between two notes and their distance in half-tones
major_chord = [ [2, 4], [2, 3] ]
minor_chord = [ [2, 3], [2, 4] ]
dom7_chord  = [ [2, 4], [2, 3], [2, 3] ]
maj7_chord  = [ [2, 4], [2, 3], [2, 4] ]
min7_chord  = [ [2, 3], [2, 4], [2, 3] ]
dim_chord   = [ [2, 3], [2, 3] ]

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

def get_chord(intervals, rootnote):
    # intervals is the list (like in major_scale[]) of intervals,
    chord = [rootnote]
    # create a list out of the notes ( [c,d,e,f,g,a,b] ):
    notes_list      = list(notes.keys())
    # get the index of the scale's rootnote:
    notes_index     = notes_list.index(rootnote[0])
    # save the previous index here so we can calculate the distance
    previous_index  = notes_index

    # walk down the intervals:
    for interval, step in intervals:
        octave_skip = False
        notes_index +=  interval
        if notes_index >= len(notes):
            notes_index = notes_index % len(notes)
            octave_skip = True
        note = notes_list[notes_index]

        # calculate the distance between the current note and the previous note
        # and add "is" or "es" if needed:
        dist_from_c      = distance_from_c(note)
        prev_dist_from_c = distance_from_c(chord[-1])
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
        chord.append(note)
    return chord

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
        scale.append(note)
    return scale

def minor_pent(scale):
    # just pass it a minor scale and remove
    # the 2nd and 6th position
    scale.remove(scale[1])
    scale.remove(scale[4])
    return scale

def major_pent(scale):
    # same as above, but pass a major scale
    # and remove the 4th and 7th position
    scale.remove(scale[3])
    scale.remove(scale[5])
    return scale

if __name__ == "__main__":
    print(get_chord(major_chord, "d"))
    print(get_chord(minor_chord, "c"))
    print(get_chord(dom7_chord, "a"))
    print(get_chord(maj7_chord, "f"))
    print(get_chord(dim_chord, "g"))
    print(get_chord(min7_chord, "dis"))
    print(get_scale(minor_scale, "bes"))
    print(get_scale(major_scale, "d"))
    print(get_scale(minor_scale, "c"))
    print(get_scale(hungarian_minor_scale, "a"))
    print(minor_pent(get_scale(minor_scale, "e")))
    print(major_pent(get_scale(major_scale, "g")))
