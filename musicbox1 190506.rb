a =
'
  2--++--++
  1++--+-+-
  '

use_synth :dsaw

b = a[1, a.length - 3].split("\n")
print b
print b.length

track2 = b[0][3..b[0].length]
track1 = b[1][3..b[1].length]

print track2
print track1

beat = 0.4

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









# for i in b do
#     track = i[2, i.length]
#     if track[0] == '1' then
#       print '111'
#       track[1, i.length].split('').each do |j|
#         play 60 if j == '-'
#         play 68 if j == '+'
#       end
#     end
#     if track[0] == '2' then
#       print '222'
#       track[1, i.length].split('').each do |j|
#         play 61 if j == '-'
#         play 69 if j == '+'
#       end
#     end
#     sleep 0.6
#     print i
#     print i[0]
#     print track
#     print track[0]
#   end

# beat = 0.4
#
# a.split('').each do |i|
#   play 66 if i == '-'
#   play 57 if i == '+'
#   sleep beat
# end
