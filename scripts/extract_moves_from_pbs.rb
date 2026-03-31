# One-off: parse Essentials-style PBS moves.txt → stdout "ID — Name" per line.
# Usage: ruby scripts/extract_moves_from_pbs.rb path/to/moves.txt

path = ARGV[0] || File.expand_path(
  "../../modcentral/the hammer/reference/pokemon-essentials/PBS/moves.txt",
  __dir__
)
abort("Missing file: #{path}") unless File.file?(path)

rows = []
cur = nil
File.foreach(path, encoding: "UTF-8") do |line|
  line = line.chomp
  if line =~ /^\[([A-Z0-9_]+)\]$/
    cur = Regexp.last_match(1)
  elsif line =~ /^Name = (.+)/ && cur
    rows << [cur, Regexp.last_match(1).strip]
    cur = nil
  end
end

out = ARGV[1]
if out && !out.empty?
  File.write(out, rows.map { |id, name| "#{id} — #{name}" }.join("\n") + "\n", encoding: "UTF-8")
  warn "Wrote #{rows.size} moves to #{out}"
else
  warn "Moves parsed: #{rows.size} (from #{path})"
  rows.each { |id, name| puts "#{id} — #{name}" }
end
