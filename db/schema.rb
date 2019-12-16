# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `rails
# db:schema:load`. When creating a new database, `rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 2019_12_07_122206) do

  create_table "card_info", id: false, force: :cascade do |t|
    t.integer "ID"
    t.text "idea"
    t.text "unit"
    t.text "obtain"
    t.text "implement"
    t.index ["ID"], name: "idindex_card_info", unique: true
  end

  create_table "card_list", id: false, force: :cascade do |t|
    t.integer "ID"
    t.text "card_name"
    t.index ["ID"], name: "idindex_card_list", unique: true
  end

  create_table "card_possession", id: false, force: :cascade do |t|
    t.integer "ID"
    t.integer "possession"
    t.index ["ID"], name: "idindex_card_possession", unique: true
  end

end
