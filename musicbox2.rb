# musicbox2


track1 = "+_ +_ "
track2 = "+   + "


rel1 = [
  ['+', '1+'],
  ['_', '1_']
]
beat1 = 0.26

rel2 = [
  ['+', '2+']
]
beat2 = beat1


in_thread do
  loop do
    sync :'1+'
    use_synth :dpulse
    play 66
  end
end

in_thread do
  loop do
    sync :'1_'
    use_synth :dpulse
    play 77
  end
end

in_thread do
  loop do
    sync :'2+'
    use_synth :bnoise
    3.times do
      play 67
      play 68
      sleep beat2/2.2
    end
  end
end


def runtrack(track, rel, beat)
  in_thread do
    loop do
      track.split('').each do |i|
        rel.each do |j|
          cue j[1] if i == j[0]
        end
        sleep beat
      end
    end
  end
end

runtrack(track1, rel1, beat1)
runtrack(track2, rel2, beat2)