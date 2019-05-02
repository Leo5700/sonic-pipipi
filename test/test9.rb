# Шумы квартир v1 190327

beat = 2.2
rate = 1
base = 800/8.0
spacing = 3

use_synth :dsaw
live_loop :a do
  notes_a = scale(hz_to_midi(base), :major_pentatonic, num_octaves: spacing)
  rate.times do
    play notes_a.choose, release: beat * (3 + rrand(-0.4, 1)), cutoff: rrand(50, 102), amp: rrand(0.8, 1)
    play notes_a.choose, release: beat * (3 + rrand(-0.4, 1)), cutoff: rrand(50, 102), amp: rrand(0.8, 1)
    sleep beat * rrand(0.99, 1.01)
  end
end

play notes_a.choose, play notes_a.choose notes_a.choose
play num_octaves p

use
