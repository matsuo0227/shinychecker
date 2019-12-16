class CardsController < ApplicationController
  def info
    id = params[:id]
    @card_info = CardInfo.find(id)
    @card_list = CardList.find(id)
  end

  def update_possession
      id = params[:id]
      pos = params[:pos]
      if pos == 'true'
          pos = 1
      else
          pos = 0
      end
      CardPossession.where(ID: id).update(possession: pos)
  end
end
