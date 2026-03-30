# Bag quantity cheat (Mods menu)

## PC install

From the `modcentral` folder:

```text
ruby bag_cheat_mod/package_mod.rb
ruby inject_mod.rb "C:\Path\To\Pokemon Fire Ash...\Game" bag_cheat_mod/mod.json
```

Back up your game first. `inject_mod.rb` creates `Data\Scripts.rxdata.bak` once.

## In game

Pause → **Mods** → pick a pocket → **Left/Right** change item, **Up/Down** ±1, **Use** type a number, **Back** returns. Mouse: click the quantity digits to type (mkxp).

## Android

See `project Vespa/fireash-scripatcher/README.md`. After `inject_mod.rb`, copy `Game/Data/Scripts.rxdata` to `fireash-scripatcher/app/src/main/assets/patched_Scripts.rxdata`, then build the APK in Android Studio.
