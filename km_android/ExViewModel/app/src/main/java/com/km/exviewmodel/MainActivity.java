package com.km.exviewmodel;

//import androidx.AppCompat


import android.arch.lifecycle.Observer;
import android.arch.lifecycle.ViewModelProviders;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;

//import androidx.lifecycle.ViewModelProviders;

public class MainActivity extends AppCompatActivity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);


//		MyViewModel viewModel = ViewModelProviders.of(this).get(MyViewModel.class);
//
//		viewModel.getUsers().observer(this, new Observer() {
//			@Override
//			public void onChanged(@Nullable User data) {
//				// update the ui.
//			}
//		});


	}
}


//package com.acme.tictactoe.view;
//
//		import android.databinding.DataBindingUtil;
//		import android.os.Bundle;
//		import android.support.v7.app.AppCompatActivity;
//		import android.view.Menu;
//		import android.view.MenuInflater;
//		import android.view.MenuItem;
//
//		import com.acme.tictactoe.R;
//		import com.acme.tictactoe.databinding.TictactoeBinding;
//		import com.acme.tictactoe.viewmodel.TicTacToeViewModel;

//public class TicTacToeActivity extends AppCompatActivity {
//
//	com.acme.tictactoe.viewmodel.TicTacToeViewModel viewModel = new com.acme.tictactoe.viewmodel.TicTacToeViewModel();
//
//	@Override
//	protected void onCreate(Bundle savedInstanceState) {
//		super.onCreate(savedInstanceState);
//		TictactoeBinding binding = DataBindingUtil.setContentView(this, R.layout.tictactoe);
//		binding.setViewModel(viewModel);
//		viewModel.onCreate();
//	}
//
//	@Override
//	protected void onPause() {
//		super.onPause();
//		viewModel.onPause();
//	}
//
//	@Override
//	protected void onResume() {
//		super.onResume();
//		viewModel.onResume();
//	}
//
//	@Override
//	protected void onDestroy() {
//		super.onDestroy();
//		viewModel.onDestroy();
//	}
//
//	@Override
//	public boolean onCreateOptionsMenu(Menu menu) {
//		MenuInflater inflater = getMenuInflater();
//		inflater.inflate(R.menu.menu_tictactoe, menu);
//		return true;
//	}
//	@Override
//	public boolean onOptionsItemSelected(MenuItem item) {
//		switch (item.getItemId()) {
//			case R.id.action_reset:
//				viewModel.onResetSelected();
//				return true;
//			default:
//				return super.onOptionsItemSelected(item);
//		}
//	}
//
//}
