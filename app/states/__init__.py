from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMFillDiary(StatesGroup):
    fill_quality_sleep = State()
    fill_drowsiness = State()
    fill_mood = State()
    fill_selffeeling_morning = State()
    fill_time_turn_bed = State()
    fill_time_turnoff_ligth = State()
    fill_time_start_sleep_minutes = State()
    fill_how_many_wakingups = State()
    fill_sum_wakingups_time_minutes = State()
    fill_time_final_wakingup = State()
    fill_wakingup_earlier = State()
    fill_wakingup_by_alam = State()
    fill_time_sleeping_night = State()
    fill_time_sleeping_day = State()
    fill_did_sport = State()
    fill_drink_alcohol = State()
    fill_use_hypnotic = State()
    fill_use_narcos = State()
    fill_meditate = State()
    fill_coffein_before_14 = State()
    fill_coffein_after_14 = State()
    fill_use_other_stimulators = State()
    fill_comment = State()


class FSMFillName(StatesGroup):
    name = State()
