#===============================================================================
# Bag quantity cheat — opened from Pause menu → Mods.
# Fire Ash / Essentials: uses $PokemonBag, Settings::BAG_MAX_PER_SLOT, GameData::Item
# Controls (item list): Left/Right = switch item, Up/Down = ±1 quantity,
#   Use/Enter = type amount, Back = return
# Mouse (mkxp): click the number to type amount.
#===============================================================================

class Window_BagCheatItemList < Window_DrawableCommand
  attr_reader :pocket_index

  def initialize(bag, pocket_index, viewport)
    @bag = bag
    @pocket_index = pocket_index
    super(0, 64, Graphics.width, Graphics.height - 64 - 80, viewport)
    if defined?(MessageConfig) && MessageConfig.const_defined?(:WINDOWSKIN)
      self.windowskin = MessageConfig::WINDOWSKIN
    end
    self.ignore_input = true if respond_to?(:ignore_input=)
    @index = 0
    refresh
  end

  def bag
    @bag
  end

  def itemCount
    arr = @bag.pockets[@pocket_index]
    return 0 if !arr

    arr.length
  end

  def pocket_entry(i)
    @bag.pockets[@pocket_index][i]
  end

  def item_id_at(index)
    e = pocket_entry(index)
    e ? e[0] : nil
  end

  def qty_at(index)
    e = pocket_entry(index)
    e ? e[1] : 0
  end

  # Hit target for the quantity column (no drawing — safe to call from input loop).
  def qty_hit_rect(index)
    full = itemRect(index)
    return nil if full.width <= 0

    inner_x = full.x + 16
    inner_w = full.width - 16
    w = 96
    Rect.new(inner_x + inner_w - w - 4, full.y, w, full.height)
  end

  def drawItem(index, _count, rect)
    entry = pocket_entry(index)
    return if !entry

    id = entry[0]
    qty = entry[1]
    itm = GameData::Item.get(id)
    rect = drawCursor(index, rect)
    left_w = rect.width - 100
    pbDrawShadowText(self.contents, rect.x, rect.y, left_w, rect.height,
                     itm.name, @baseColor, @shadowColor, 0)
    qty_x = rect.x + left_w
    pbDrawShadowText(self.contents, qty_x, rect.y, 22, rect.height,
                     _INTL("▼"), @baseColor, @shadowColor, 1)
    pbDrawShadowText(self.contents, qty_x + 22, rect.y, 44, rect.height,
                     qty.to_s, @baseColor, @shadowColor, 1)
    pbDrawShadowText(self.contents, qty_x + 66, rect.y, 22, rect.height,
                     _INTL("▲"), @baseColor, @shadowColor, 1)
  end
end

#===============================================================================
#
#===============================================================================
class PokemonBagCheat_Scene
  def initialize
    @bag = $PokemonBag
    @viewport = nil
    @sprites = {}
    @mode = :pockets
    @pocket_commands = nil
    @pocket_indices = nil
  end

  def pbStartScene
    @viewport = Viewport.new(0, 0, Graphics.width, Graphics.height)
    @viewport.z = 99999
    @sprites = {}
    @mode = :pockets
    build_pocket_menu
    @sprites["help"] = Window_UnformattedTextPokemon.newWithSize(
      _INTL(""),
      0, Graphics.height - 80, Graphics.width, 80, @viewport
    )
    pbRefreshHelp
    pbFadeInAndShow(@sprites) { pbUpdate }
  end

  def pbRefreshHelp
    w = @sprites["help"]
    return unless w

    if @mode == :pockets
      w.text = _INTL("Choose a pocket. Press Back to close.")
    else
      w.text = _INTL("Left/Right: item  Up/Down: ±1  Use: type amount  Click number: type (mouse)  Back: pockets")
    end
    w.resizeToFit(w.text, Graphics.width)
    w.y = Graphics.height - w.height
  end

  def build_pocket_menu
    dispose_item_list
    @sprites["pocketcmd"]&.dispose
    @pocket_indices = []
    commands = []
    (1..PokemonBag.numPockets).each do |pi|
      pname = Settings.bag_pocket_names[pi]
      n = @bag.pockets[pi].length
      commands.push(_INTL("{1} ({2} stacks)", pname, n))
      @pocket_indices.push(pi)
    end
    @sprites["pocketcmd"] = Window_CommandPokemon.new(commands, Graphics.width)
    @sprites["pocketcmd"].viewport = @viewport
    @sprites["pocketcmd"].x = 0
    @sprites["pocketcmd"].y = 0
    @sprites["pocketcmd"].z = 2
    @sprites["pocketcmd"].height = [@sprites["pocketcmd"].height, Graphics.height - 80].min
    @mode = :pockets
    pbRefreshHelp
  end

  def dispose_item_list
    if @sprites["itemlist"]
      @sprites["itemlist"].dispose
      @sprites.delete("itemlist")
    end
    @sprites["title"]&.dispose
    @sprites.delete("title")
  end

  def open_pocket(pocket_index)
    dispose_item_list
    @sprites["pocketcmd"].visible = false
    @sprites["pocketcmd"].active = false
    @current_pocket = pocket_index
    title = Settings.bag_pocket_names[pocket_index]
    @sprites["title"] = Window_UnformattedTextPokemon.newWithSize(
      title.to_s, 0, 0, Graphics.width, 56, @viewport
    )
    @sprites["itemlist"] = Window_BagCheatItemList.new(@bag, pocket_index, @viewport)
    @sprites["itemlist"].z = 2
    @sprites["itemlist"].active = true
    @sprites["itemlist"].index = 0
    @sprites["itemlist"].refresh
    @mode = :items
    if @sprites["itemlist"].itemCount == 0
      pbMessage(_INTL("No items in this pocket."))
      close_pocket
    else
      pbRefreshHelp
    end
  end

  def close_pocket
    dispose_item_list
    @sprites["pocketcmd"].visible = true
    @sprites["pocketcmd"].active = true
    @mode = :pockets
    pbRefreshHelp
  end

  def pbApplyQtyDelta(delta)
    w = @sprites["itemlist"]
    return if !w || w.itemCount == 0

    i = w.index
    id = w.item_id_at(i)
    return if !id

    item = GameData::Item.get(id)
    oldq = w.qty_at(i)
    maxq = Settings::BAG_MAX_PER_SLOT
    newq = (oldq + delta).clamp(0, maxq)
    return if newq == oldq

    if newq > oldq
      @bag.pbStoreItem(item, newq - oldq)
    else
      @bag.pbDeleteItem(item, oldq - newq)
    end
    pbPlayCursorSE
    w.refresh
  end

  def pbPromptQuantity
    w = @sprites["itemlist"]
    return if !w || w.itemCount == 0

    i = w.index
    id = w.item_id_at(i)
    return if !id

    item = GameData::Item.get(id)
    oldq = w.qty_at(i)
    params = ChooseNumberParams.new
    params.setRange(0, Settings::BAG_MAX_PER_SLOT)
    params.setDefaultValue(oldq)
    newq = pbMessageChooseNumber(
      _INTL("New quantity for {1} (max. {2}).", item.name, Settings::BAG_MAX_PER_SLOT),
      params
    ) { pbUpdate }
    newq = newq.clamp(0, Settings::BAG_MAX_PER_SLOT)
    return if newq == oldq

    if newq > oldq
      @bag.pbStoreItem(item, newq - oldq)
    elsif newq < oldq
      @bag.pbDeleteItem(item, oldq - newq)
    end
    pbPlayDecisionSE
    w.refresh
  end

  def pbTryMouseQtyClick
    return if !defined?(Mouse)
    return if !Input.respond_to?(:MOUSELEFT) || !Input.trigger?(Input::MOUSELEFT)

    pos = Mouse.getMousePos rescue nil
    return if !pos || !pos[0]

    mx = pos[0]
    my = pos[1]
    w = @sprites["itemlist"]
    return if !w || w.itemCount == 0

    (0...w.itemCount).each do |idx|
      r = w.qty_hit_rect(idx)
      next if !r
      wx = w.x + (w.viewport ? w.viewport.rect.x : 0)
      wy = w.y + (w.viewport ? w.viewport.rect.y : 0)
      if mx >= wx + r.x && mx < wx + r.x + r.width && my >= wy + r.y && my < wy + r.y + r.height
        w.index = idx
        w.refresh
        pbPromptQuantity
        break
      end
    end
  end

  def pbUpdate
    pbUpdateSpriteHash(@sprites)
    pbUpdateSceneMap
  end

  def pbMain
    loop do
      Graphics.update
      Input.update
      pbUpdate
      if @mode == :pockets
        @sprites["pocketcmd"].update
        if Input.trigger?(Input::BACK)
          break
        elsif Input.trigger?(Input::USE)
          i = @sprites["pocketcmd"].index
          pi = @pocket_indices[i]
          pbPlayDecisionSE
          open_pocket(pi)
        end
      elsif @mode == :items
        w = @sprites["itemlist"]
        w.update if w
        pbTryMouseQtyClick
        if Input.trigger?(Input::BACK)
          pbPlayCloseMenuSE
          close_pocket
        elsif w && w.itemCount > 0
          if Input.repeat?(Input::LEFT)
            w.index = (w.index - 1 + w.itemCount) % w.itemCount
            pbPlayCursorSE
            w.refresh
          elsif Input.repeat?(Input::RIGHT)
            w.index = (w.index + 1) % w.itemCount
            pbPlayCursorSE
            w.refresh
          elsif Input.repeat?(Input::UP)
            pbApplyQtyDelta(1)
          elsif Input.repeat?(Input::DOWN)
            pbApplyQtyDelta(-1)
          elsif Input.trigger?(Input::USE)
            pbPromptQuantity
          end
        end
      end
    end
  end

  def pbEndScene
    pbPlayCloseMenuSE
    pbFadeOutAndHide(@sprites) { pbUpdate }
    pbDisposeSpriteHash(@sprites)
    @viewport.dispose
  end
end

#===============================================================================
#
#===============================================================================
class PokemonBagCheatScreen
  def initialize(scene)
    @scene = scene
  end

  def pbStartScreen
    if !$PokemonBag
      pbMessage(_INTL("The bag is not available right now."))
      return
    end
    @scene.pbStartScene
    @scene.pbMain
    @scene.pbEndScene
  end
end
