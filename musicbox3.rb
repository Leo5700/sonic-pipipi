track3 = "+   -  _"
track2 = "---  +++"
track1 = "- + - + "

beat = 0.14


use_synth :bnoise

live_loop :t4 do
  notes = scale(:a2, :minor_pentatonic, num_octaves: 1)
  play notes.choose, release: 0.1
  # play notes.choose, release: beat * (3 + rrand(-0.4, 1)), cutoff: rrand(50, 102), amp: rrand(0.8, 1)
  sleep beat/2
end

use_synth :growl

live_loop :t3 do
  track3.split('').each do |i|
    play chord(:c3, :minor), sustain: 0.6, amp: rrand(0.5, 2.2) if i == '+'
    play chord(:a5, :minor), sustain: 0.5, amp: rrand(0.5, 2.8) if i == '-'
    play chord(:d4, :minor), release: 0.4, amp: rrand(0.5, 2.7) if i == '_'
    sleep beat * rrand(0.999, 1.001)
  end
end

use_synth :gnoise

live_loop :t2 do
  sleep beat * 10
  track2.split('').each do |i|
    play chord(:a3, :minor) if i == '-'
    play chord(:a4, :minor) if i == '+'
    sleep beat * rrand(0.999, 1.001)
  end
end

live_loop :t1 do
  sleep beat * 10
  track1.split('').each do |i|
    play chord(:c3, :minor) if i == '-'
    play chord(:c4, :minor) if i == '+'
    sleep beat * rrand(0.999, 1.001)
  end
end
