Rails.application.routes.draw do
  get 'home/index'
  post 'cards/update_possession'
  get 'cards/info'
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
  get ':controller(/:action(/:id))(.:format)'
end
