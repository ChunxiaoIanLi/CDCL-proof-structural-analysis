/*
 * Copyright (C) 2006 
 * Thomas van Dijk
 * Jan-Pieter van den Heuvel
 * Wouter Slob
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */
 
package nl.uu.cs.treewidth;

import java.io.File;
import java.net.URL;
import java.util.ArrayList;

import nl.uu.cs.treewidth.algorithm.Algorithm;
import nl.uu.cs.treewidth.algorithm.Exact;
import nl.uu.cs.treewidth.algorithm.LowerBound;
import nl.uu.cs.treewidth.algorithm.Permutation;
import nl.uu.cs.treewidth.algorithm.UpperBound;
import nl.uu.cs.treewidth.input.DgfReader;
import nl.uu.cs.treewidth.input.GraphInput;
import nl.uu.cs.treewidth.input.InputException;
import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.timing.JavaNanoTime;
import nl.uu.cs.treewidth.timing.Stopwatch;

public class AlgoTester {

	static boolean verbose = false;
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
		// Hello.
		System.out.println( "          #=========================================================#" );
		System.out.println( "          #                       AlgoTester                        #" );
		System.out.println( "          #                      for the win!                       #" );
		System.out.println( "          #=========================================================#" );
		System.out.println( "" );
		
		String graphFile;
		if( args.length==0 )
			graphFile = "graphs/celar02.dgf";
		else
			graphFile = args[0];
		
		// Get a test graph.
		GraphInput input = new DgfReader(graphFile);
		NGraph<InputData> g = null;
		try {
			g = input.get();
		} catch( InputException e ) {
			System.out.println( "Uncaught exception while reading graph. Urgh, dying." );
			e.printStackTrace();
			System.exit(1);
		}
		
		// Packages to look in for classes.
		String[] packages = {
			"nl.uu.cs.treewidth.algorithm"
		};
		
		// Get all the classes in the packages.
		ArrayList<String> classes = new ArrayList<String>();
		for( String packageName : packages ) {
			try {
				classes.addAll( getClasses( packageName ) );
			} catch( ClassNotFoundException e ) {
				e.printStackTrace();
			}
		}
		
		classes.clear();
		classes.add( "nl.uu.cs.treewidth.algorithm.MaximumMinimumDegreePlusLeastC" );
		
		System.out.println("Number of classes: " + classes.size());
		
		// Test all the classes.
		for( String className : classes ) {
			AlgoTester.test( className, g );
		}
		
			
		// Bye.
		System.out.println();
		System.out.println( "          #=========================================================#" );
		System.out.println( "          #                     Done, Goodbye!                      #" );
		System.out.println( "          #=========================================================#" );
		
	}
	
	public static ArrayList<String> getClasses( String packageName ) throws ClassNotFoundException {
		
		ArrayList<String> classes = new ArrayList<String>();
		
		// Get a File object for the package
		File directory = null;
		try {
			ClassLoader cld = Thread.currentThread().getContextClassLoader();
			if (cld == null) {
				throw new ClassNotFoundException("Can't get class loader.");
			}
			String path = packageName.replace('.', '/');
			URL resource = cld.getResource(path);
			if( resource == null ) {
				throw new ClassNotFoundException("No resource for " + path);
			}
			directory = new File( resource.getFile() );
		} catch (NullPointerException x) {
			throw new ClassNotFoundException(packageName + " (" + directory + ") does not appear to be a valid package" );
		}
		
		if( directory.exists() ) {
			// Get the list of the files contained in the package
			String[] files = directory.list();
			for( int i = 0; i<files.length; i++ ) {
				// we are only interested in .class files
				if( files[i].endsWith(".class") ) {
					// removes the .class extension
					String className = files[i].substring(0, files[i].length() - 6);
					if(!className.equals("TreewidthDP") &&
					   !className.equals("TreewidthDP2") &&
					   !className.equals("TreewidthDP3") &&
					   !className.equals("QuickBB") &&
					   !className.equals("QuickBB2") &&
					   !className.equals("QuickBB3")
					   )
					classes.add( packageName + '.' + className );
				}
			}
		} else {
			throw new ClassNotFoundException( packageName + " does not appear to be a valid package");
		}
		return classes;
	}

	
	public static void test( String typeName, NGraph<InputData> g ) {
		AlgoTester tester = new AlgoTester( typeName );
		
		if( tester.isValidAlgorithm() ) {
			tester.test( g );
			System.out.println();
		}
	}
	
	
	String typeName;
	Algorithm<InputData> a;
	
	AlgoTester( String typeName ) {
		
		a = null;
		this.typeName = typeName;
		ClassLoader loader = ClassLoader.getSystemClassLoader();
		Class c = null;
		try {
			c = loader.loadClass( typeName );
		} catch (ClassNotFoundException e) {
			if(verbose) System.out.println( "-> Dude, " + typeName + " isn't even a type!\n" );
			return;
		}
		Object o = null;
		try {
			o = c.newInstance();
		} catch (InstantiationException e) {
			if(verbose) System.out.println( "-> Failed to instantiate " + typeName + "\n" );
			return;
		} catch (IllegalAccessException e) {
			if(verbose) System.out.println( "-> Access to " + typeName + " not legal.\n" );
			return;
		} 
		
		if( o instanceof Algorithm ) {			
			a = (Algorithm<InputData>)o;
		} else {
			if(verbose) System.out.println( "-> Wait a minute! " + typeName + " isn't an Algorithm!\n" );
		}
	}
	boolean isValidAlgorithm() {
		return a!=null;
	}
	
	void test( NGraph<InputData> g ) {
				
		System.out.println( "-> " + typeName + "\n   " + a.getName() );
		Stopwatch t = new Stopwatch( new JavaNanoTime() );
		t.start();
		try {
			a.setInput( g );
			a.run();
		} catch( Error e ) {
			System.out.println( "   [-- Java completely borked out on this one. Compile errors? Corrupt class files? --]" );
			return;
		}
		t.stop();
		System.out.println( "   Time for one run: " + t.getTime() + " ms." );
		if( a instanceof LowerBound ) {
			LowerBound<InputData> lb = (LowerBound<InputData>)a;
			System.out.println( "   + It is a LowerBound and gives " + lb.getLowerBound() );
		}
		if( a instanceof UpperBound ) {
			UpperBound<InputData> ub = (UpperBound<InputData>)a;
			System.out.println( "   + It is an UpperBound and gives " + ub.getUpperBound() );
		}
		if( a instanceof Exact ) {
			Exact<InputData> e = (Exact<InputData>)a;
			System.out.println( "   + It is an Exact and gives " + e.getTreewidth() );
		}
		if( a instanceof Permutation ) {
			Permutation<InputData> p = (Permutation<InputData>)a;
			System.out.println( "   + It is a Permutation and gives " + p.getPermutation().toString() );
		}
		
	}
	

}
