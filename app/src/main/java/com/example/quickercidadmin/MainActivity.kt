package com.example.quickercidadmin

import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.quickercidadmin.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // View Binding 설정
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // 비밀번호 입력 처리
        binding.etPassword.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            
            override fun afterTextChanged(s: Editable?) {
                // 비밀번호 입력 여부에 따라 로그인 버튼 활성화/비활성화
                binding.btnLogin.isEnabled = !s.isNullOrEmpty()
            }
        })

        // 로그인 버튼 클릭 이벤트
        binding.btnLogin.setOnClickListener {
            val password = binding.etPassword.text.toString()
            if (password.isNotEmpty()) {
                // 로딩 표시
                binding.progressBar.visibility = View.VISIBLE
                
                // 로그인 처리
                attemptLogin(password)
            }
        }

        // 초기 상태에서는 로그인 버튼 비활성화
        binding.btnLogin.isEnabled = false
    }

    private fun attemptLogin(password: String) {
        // TODO: 서버 통신 구현
        // 임시로 토스트 메시지 표시
        Toast.makeText(this, "로그인 시도: $password", Toast.LENGTH_SHORT).show()
        binding.progressBar.visibility = View.GONE
    }
} 