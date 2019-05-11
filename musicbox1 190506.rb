track2 = "--++--++"
track1 = "+ +--+-+-"

use_synth :bnoise

beat = 0.18

live_loop :t2 do
  track2.split('').each do |i|
    play 44 if i == '-'
    play 77 if i == '+'
    sleep beat
  end
end

live_loop :t1 do
  track1.split('').each do |i|
    play 56 if i == '-'
    play 58 if i == '+'
    sleep beat
  end
end
