'''
# Шумы квартир v1 190327

beat = 2.6
rate = 1
base = 25  # Hz
spacing = 5

print base
use_synth :dsaw
live_loop :a do
  notes_a = scale(hz_to_midi(base), :major_pentatonic, num_octaves: spacing)
  rate.times do
    play notes_a.choose, release: beat * (3 + rrand(-0.4, 1)), cutoff: rrand(50, 102), amp: rrand(0.8, 1)
    play notes_a.choose, release: beat * (3 + rrand(-0.4, 1)), cutoff: rrand(50, 102), amp: rrand(0.8, 1)
    sleep beat * rrand(0.99, 1.01)
  end
end
'''


import psonic as ps
import librosa as lr
import random


beat = 2.6
rate = 1
base = 25  # Hz
spacing = 5
print(base)
ps.use_synth(ps.DSAW)
while True:
    for i in range(rate):
        notes = ps.scale(lr.hz_to_midi(base),
                         'major_pentatonic',
                         num_octaves = spacing)
        for j in range(2):
            ps.play(random.choice(notes),
                    release = beat * (3 + random.uniform(-0.4, 1)),
                    cutoff = random.uniform(50, 102),
                    amp = random.uniform(0.8, 1))
        ps.sleep(beat * random.uniform(0.99, 1.01))

