class HomeController < ApplicationController
    helper_method :return_possession
  def index
      @pSSR_id_thums = get_thums('pSSR')
      @pSR_id_thums = get_thums('pSR')
      @pR_id_thums = get_thums('pR')
      @sSSR_id_thums = get_thums('sSSR')
      @sSR_id_thums = get_thums('sSR')
      @sR_id_thums = get_thums('sR')
      @sN_id_thums = get_thums('sN')
  end

  def get_thums(type)
      path = "./app/assets/images/icon/#{type}/*.jpg"
      thums = Dir.glob(path).sort.map do |thum|
          "/assets/icon/#{type}/#{File.basename(thum)}"
      end
      ids = thums.map { |thum| File.basename(thum, '.jpg').to_i() }
      id_thums = thums.zip(ids).map { |id_thum|
          { :id => id_thum[1], :thum => id_thum[0] }
      }
      return id_thums
  end

  def return_possession(id)
      pos = CardPossession.find(id)['possession']
      if pos == 0
          return ['false', '']
      else
          return ['true', 'checked']
      end
  end
end
