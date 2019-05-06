# musicbox1 0.2

track2 = "--++--++"
track1 = "+ +--+-+-"

use_synth :hollow

beat = 0.18

live_loop :t2 do
  ampr = rrand(0.33, 0.66)
  track2.split('').each do |i|
    play 44 if i == '-'
    play 77, amp: ampr if i == '+'
    sleep beat * rrand(0.999, 1.001)
  end
end

live_loop :t1 do
  track1.split('').each do |i|
    play 56 if i == '-'
    play 58 if i == '+'
    sleep beat * rrand(0.999, 1.001)
  end
end

beatshift = 0.14
live_loop :beat do
  sleep beat * beatshift
  with_fx :echo, mix: 0.1, phase: 0.107 do
    sample :bass_hit_c, rate: 0.5, amp: 0.2
  end
  sleep beat * (4 - beatshift)
end
