#!/usr/bin/env ruby
# Writes mod.json next to this script for inject_mod.rb
require "json"

dir = __dir__
pause = File.read(File.join(dir, "UI_PauseMenu.rb"), encoding: "UTF-8")
cheat = File.read(File.join(dir, "UI_Mod_BagCheat.rb"), encoding: "UTF-8")

mod = {
  "files" => [
    {
      "scriptName" => "UI_PauseMenu",
      "content" => pause
    },
    {
      "scriptName" => "UI_Mod_BagCheat",
      "content" => cheat,
      "appendIfMissing" => true
    }
  ]
}

out = File.join(dir, "mod.json")
File.write(out, JSON.pretty_generate(mod), encoding: "UTF-8")
puts "Wrote #{out}"
