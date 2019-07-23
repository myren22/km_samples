package com.journaldev.nested;

import java.util.Arrays;
//nested classes can be used in import for easy instantiation
import com.journaldev.nested.OuterClass.InnerClass;
import com.journaldev.nested.OuterClass.StaticNestedClass;

public class InnerClassTest {

    public static void main(String[] args) {
//    	StaticNestedClass staticNestedClass3;
//    	System.out.println(StaticNestedClass3.f); 
    	//staticNestedClass3 = new StaticNestedClass();
        
//        System.out.println(staticNestedClass3.getName());
    	
    	OuterClass outer = new OuterClass(1,2,3,4);
        
        //static nested classes example
        StaticNestedClass staticNestedClass = new StaticNestedClass();
        StaticNestedClass staticNestedClass1 = new StaticNestedClass();
        
        System.out.println(staticNestedClass.getName());
        staticNestedClass.d=10;
        System.out.println(staticNestedClass.d);
        System.out.println(staticNestedClass1.d);
        
        //inner class example
        InnerClass innerClass = outer.new InnerClass();
        System.out.println(innerClass.getName());
        System.out.println(innerClass);
        innerClass.setValues();
        System.out.println(innerClass);
        System.out.println("======");
        System.out.println(outer);
        
        //calling method using local inner class
        outer.print("Outer");
        
        //calling method using anonymous inner class
        System.out.println(Arrays.toString(outer.getFilesInDir("src/com/journaldev/nested", ".java")));
        
        System.out.println(Arrays.toString(outer.getFilesInDir("bin/com/journaldev/nested", ".class")));
    }

}
