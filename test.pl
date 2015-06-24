#!/usr/bin/perl
use strict;
sub test {
    my $t;
    {
        open In, "test.html" or die "Can't open test.html.\n";
        local $/;
        $t=<In>;
        close In;
    }
    my $root_node = parse_html($t);
    debug_dom($root_node);
}

sub parse_html {
    my ($l) = @_;
    my @tag_stack;
    my $cur_list=[];
    push @tag_stack, {'_name'=>'root', '_list'=>$cur_list};
    my $n=length($l);
    while(pos($l)<$n){
        if($l=~/\G<!--.*-->/gci){
            next;
        }
        if($l=~/\G<!DOCTYPE.*?>/gci){
            next;
        }
        if($l=~/\G[^<]+/gci){
            push @$cur_list, $&;
            next;
        }
        if($l=~/\G<(\w+)(.*?)>/gci){
            my ($name, $attr)=($1, $2);
            my $tag = {'_name'=>$name};
            parse_attribute($tag, $attr);
            push @$cur_list, $tag;
            if($tag->{'/'} or $name=~/^(area|base|br|col|embed|hr|img|input|keygen|link|meta|param|source|track|wbr)$/i){
            }
            elsif($name=~/^(script|style|textarea|title)$/i){
                if($l=~/\G(.*?)<\/$name\b.*?>/gci){
                    $tag->{_text}=$1;
                }
            }
            else{
                push @tag_stack, $tag;
                $cur_list=[];
                $tag->{'_list'} = $cur_list;
            }
            next;
        }
        if($l=~/\G<\/(\w+).*?>/gci){
            my $name=$1;
            if($name eq $tag_stack[-1]->{'_name'}){
                pop @tag_stack;
                $cur_list=$tag_stack[-1]->{'_list'};
            }
            else{
                my $j=$#tag_stack-1;
                while($j>0){
                    if($name eq $tag_stack[$j]->{'_name'}){
                        while(@tag_stack>=$j){
                            pop @tag_stack;
                        }
                        $cur_list=$tag_stack[-1]->{'_list'};
                        last;
                    }
                    $j--;
                }
            }
            next;
        }
        $l=~/\G./gc;
    }
    return $tag_stack[0];
}

sub parse_attribute {
    my ($tag, $attr) = @_;
    my $n=length($attr);
    while(pos($attr)<$n){
        if($attr=~/\G\s+/gci){
            next;
        }
        if($attr=~/\G\//gci){
            $tag->{'/'}=1;
            next;
        }
        if($attr=~/\G([^\s'"\\=<>`]+)/gci){
            my $name=$1;
            if($attr=~/\G\s*=\s*/gci){
                while(pos($attr)<$n){
                    if($attr=~/\G"((?:[^\\"]+|\\.)*)"/gci){
                        $tag->{name}=$1;
                        last;
                    }
                    if($attr=~/\G'((?:[^\\']+|\\.)*)'/gci){
                        $tag->{name}=$1;
                        last;
                    }
                    if($attr=~/\G[^\s'"=<>`]+/gci){
                        $tag->{name}=$&;
                        last;
                    }
                    $attr=~/\G./gc;
                }
            }
            else{
                $tag->{$name}=1;
            }
            next;
        }
    }
}

sub debug_dom {
    my ($node) = @_;
    print_node($node, 0);
}

sub print_node {
    my ($node, $level) = @_;
    if(ref($node) ne "HASH"){
        print "    " x $level, $node, "\n";
    }
    else{
        print "    " x $level, $node->{'_name'}, "\n";
        if($node->{_list}){
            foreach my $t (@{$node->{'_list'}}){
                print_node($t, $level+1);
            }
        }
    }
}

test();
