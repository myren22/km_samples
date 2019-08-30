This project created as a replica of this code: https://www.journaldev.com/21168/android-livedata

ViewModels are meant to hold LiveData objects. LiveData objects notify
their obeservers when their data is changed.

ViewModel is aware of the LifeCycle state[Pause,Resume,Delete], and will only update
the data if in a state where the changes would be visible.