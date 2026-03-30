#!/usr/bin/env ruby
# frozen_string_literal: true

# Verifies that Data/Scripts.rxdata matches Pokémon Fire Ash 3.6 Part 2.2 (supported target).
# Used before inject_mod.rb from sync_patched_scripts_to_apk.ps1.
#
# Usage: ruby verify_fire_ash_scripts_version.rb path/to/Data/Scripts.rxdata
# Exit 0 = OK, 1 = unsupported / unreadable.

require "zlib"

SUPPORTED_LABEL = "Pokémon Fire Ash 3.6 Part 2.2"

def combined_script_text(rxdata_path)
  raw = File.binread(rxdata_path)
  data = Marshal.load(raw)
  raise "Unexpected Scripts.rxdata root type: #{data.class}" unless data.is_a?(Array)

  parts = []
  data.each do |entry|
    next unless entry.is_a?(Array)

    # RMXP / Essentials rows are usually [magic, name, zlib_source], but try every String cell.
    entry.each do |cell|
      next unless cell.is_a?(String)
      next if cell.length < 8

      begin
        src = Zlib::Inflate.inflate(cell)
      rescue Zlib::DataError
        next
      end
      parts << src.force_encoding("UTF-8")
    end
  end
  parts.join("\n")
end

def matches_supported_fire_ash?(text)
  return false if text.nil? || text.empty?

  t = text.encode("UTF-8", invalid: :replace, undef: :replace)
  part22 = t.match?(/part\s*2\.2/i)
  ver36 = t.match?(/3\.6/)
  fireash = t.match?(/fire\s*ash/i) || t.match?(/fireash/i)
  part22 && ver36 && fireash
end

path = ARGV[0]
if path.nil? || path.strip.empty?
  warn "Usage: ruby verify_fire_ash_scripts_version.rb <path/to/Scripts.rxdata>"
  exit 1
end

unless File.file?(path)
  warn "Not a file: #{path}"
  exit 1
end

begin
  combined = combined_script_text(path)
rescue StandardError => e
  warn "Could not read Scripts.rxdata (wrong format or corrupt): #{e.message}"
  exit 1
end

if matches_supported_fire_ash?(combined)
  puts "OK: Scripts.rxdata matches expected markers for #{SUPPORTED_LABEL}."
  exit 0
end

warn <<~MSG
  UNSUPPORTED: #{path}
  This mod and APK are built for **#{SUPPORTED_LABEL}** only.

  Decompressed scripts did not all contain the expected signatures:
    - text like "Part 2.2" (case-insensitive)
    - "3.6"
    - "Fire Ash" or "FireAsh"

  Use the correct game version, or pass -SkipVersionCheck on sync_patched_scripts_to_apk.ps1 only if you accept the risk.
MSG
exit 1
