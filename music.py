#!/usr/bin/env python3

# by Christoph Barth 2019
# a simple script that generates a scale on a given root

# FIXME: some note names are not correct, for example "ees" should be "es", 
#        since I am aiming at lilypond-output and this seems to be ok,
#        this will not be fixed I think. Maybe I'll add some conversion function
#        that makes "c-flat" out of "ces"...
#        see here: http://lilypond.org/doc/v2.18/Documentation/music-glossary/pitch-names
#        and here: http://lilypond.org/doc/v2.18/Documentation/notation/writing-pitches#note-names-in-other-languages

# TODO: add more chords/scales, argparse so we can actually use this
#       for something useful :)
# scales to implement:
#   whole tone scale
#   altered scale

# the note names. The second value is their relative distance to c
# so we know when to use flat/sharp notes:
notes     = { 'c': 0,
              'd': 2,
              'e': 4,
              'f': 5,
              'g': 7,
              'a': 9,
              'b':11 }

# scales and chords are stored in a nested list with 2 elements:
# the step between two notes (1 = one step up = c-d, e-f etc.)
# and their distance in half-tones

# define some scales:

# major scale:
major_scale = [ [1, 2], [1, 2], [1, 1], [1, 2], [1, 2], [1, 2], [1, 1] ]
# major pentatonic:
major_pent  = [ [1, 2], [1, 2], [2, 3], [1, 2], [2, 3] ]
# minor scale:
minor_scale = [ [1, 2], [1, 1], [1, 2], [1, 2], [1, 1], [1, 2], [1, 2] ]
# harmonic minor scale:
harmonic_minor_scale = [ [1, 2], [1, 1], [1, 2], [1, 2], [1, 1], [1, 3], [1, 1] ]
# minor pentatonic:
minor_pent  = [ [2, 3], [1, 2], [1, 2], [2, 3], [1, 2] ]
# hungarian minor:
hungarian_minor_scale = [ [1, 2], [1, 1], [1, 3], [1, 1], [1, 1], [1, 3], [1, 1] ]

# modes:
ionian_scale = major_scale
dorian_scale = ionian_scale[1:]
dorian_scale.append(ionian_scale[0])
phrygian_scale = dorian_scale[1:]
phrygian_scale.append(dorian_scale[0])
lydian_scale = phrygian_scale[1:]
lydian_scale.append(phrygian_scale[0])
mixolydian_scale = lydian_scale[1:]
mixolydian_scale.append(lydian_scale[0])
aeolian_scale = minor_scale
locrian_scale = minor_scale[1:]
locrian_scale.append(minor_scale[0])

# chords:
major_chord = [ [2, 4], [2, 3] ]
minor_chord = [ [2, 3], [2, 4] ]
dom7_chord  = [ [2, 4], [2, 3], [2, 3] ]
maj7_chord  = [ [2, 4], [2, 3], [2, 4] ]
min7_chord  = [ [2, 3], [2, 4], [2, 3] ]
dim_chord   = [ [2, 3], [2, 3] ]
aug_chord   = [ [2, 4], [2, 4] ]
ninth_chord = [ [2, 4], [2, 3], [2, 3], [2, 4] ]

# specials:

# circle of fifths:
circle_of_fifths      = [ [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7], [4, 7] ]
circle_of_fifths_flat = [ [3, 5], [3, 5], [3, 5], [3, 5], [3, 5], [3, 5], [3, 5], [3, 5] ]

# parallel major/minor:
parallel_major = [ [2, 3] ]
parallel_minor = [ [5, 9] ]

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

def get_notes(intervals, rootnote):
    # intervals is the list (like in major_scale[]) of intervals,
    ret_notes = [rootnote]
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
        prev_dist_from_c = distance_from_c(ret_notes[-1])
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
        ret_notes.append(note)
    return ret_notes

if __name__ == "__main__":
    print("examples:\n")
    print("e minor parallel -> {} major". format(get_notes(parallel_major, "e")[1]))
    print("b major parallel -> {} minor". format(get_notes(parallel_minor, "b")[1]))
    print("circle of fifths (#): ", *get_notes(circle_of_fifths, "c"))
    print("circle of fifths (b): ", *get_notes(circle_of_fifths_flat, "c"))
    print("d major chord: ", *get_notes(major_chord, "d"))
    print("c minor chord: ", *get_notes(minor_chord, "c"))
    print("a dominant7 chord: ", *get_notes(dom7_chord, "a"))
    print("f major7 chord: ", *get_notes(maj7_chord, "f"))
    print("g diminished chord: ", *get_notes(dim_chord, "g"))
    print("dis minor7 chord: ", *get_notes(min7_chord, "dis"))
    print("c augmented chord: ", *get_notes(aug_chord, "c"))
    print("g ninth chord: ", *get_notes(ninth_chord, "g"))
    print("d major scale: ", *get_notes(major_scale, "d"))
    print("cis minor scale: ", *get_notes(minor_scale, "cis"))
    print("a harmonic minor scale: ", *get_notes(harmonic_minor_scale, "a"))
    print("a hungarian minor scale: ", *get_notes(hungarian_minor_scale, "a"))
    print("e minor pentatonic: ", *get_notes(minor_pent, "e"))
    print("a major pentatonic: ", *get_notes(major_pent, "a"))
    print("e ionian scale: ", *get_notes(ionian_scale, "e"))
    print("e dorian scale: ", *get_notes(dorian_scale, "e"))
    print("e phrygian scale: ", *get_notes(phrygian_scale, "e"))
    print("e lydian scale: ", *get_notes(lydian_scale, "e"))
    print("e mixolydian scale: ", *get_notes(mixolydian_scale, "e"))
    print("e aeolian scale: ", *get_notes(aeolian_scale, "e"))
    print("e locrian scale: ", *get_notes(locrian_scale, "e"))
